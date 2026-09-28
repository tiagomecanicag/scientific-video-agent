"""Initialise a project or check its records. Standard library only; no network calls."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PureWindowsPath
import sys

SKILL = Path(__file__).resolve().parents[1]
FOLDERS = ('01_sources', '02_script', '03_references', '04_animatic', '05_segments',
           '06_edit', '07_export', '08_publication', '09_documentation')
STATUSES = {'pending', 'in_progress', 'awaiting_approval', 'approved', 'needs_revision'}


def init_project(directory, language, title):
    root = Path(directory).expanduser().resolve()
    if root == SKILL or SKILL in root.parents:
        raise ValueError('Project outputs must be outside the installed skill.')
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise ValueError('Destination is not empty. Resume it or choose a new folder; nothing was overwritten.')
    state = json.loads((SKILL / 'assets/project_state.template.json').read_text(encoding='utf-8'))
    state.update(project_id=root.name, title=title, language=language,
                 created_at=datetime.now(timezone.utc).isoformat())
    root.mkdir(parents=True, exist_ok=True)
    for name in FOLDERS:
        (root / name).mkdir()
    (root / 'project_state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    log = (SKILL / f'references/{language}/CONTINUITY_LOG.txt').read_text(encoding='utf-8')
    heading = 'Registro de continuidade' if language == 'pt' else 'Continuity Log'
    (root / 'CONTINUITY.md').write_text(f'# {heading}\n\n{title}\n\n{log}', encoding='utf-8')
    return root


def approval_matches(record, scope):
    return bool(record.get('version')) and any(
        a.get('decision') == 'approved' and a.get('version') == record.get('version')
        and a.get('scope') == scope and str(a.get('user_message') or '').strip()
        and a.get('recorded_at')
        for a in record.get('approvals', []) if isinstance(a, dict))


def check_project(directory):
    root = Path(directory).expanduser().resolve()
    state = json.loads((root / 'project_state.json').read_text(encoding='utf-8'))
    errors, warnings = [], []

    def error(message):
        errors.append(message)

    def artifact(item, label, required=False):
        if not item:
            if required: error(f'{label}: missing artifact.')
            return None
        if not isinstance(item, dict) or not isinstance(item.get('path'), str):
            error(f'{label}: expected a path and SHA-256 object.')
            return None
        name = item['path']
        if Path(name).is_absolute() or PureWindowsPath(name).is_absolute():
            error(f'{label}: use a relative project path.')
            return None
        target = (root / name).resolve()
        if root not in target.parents:
            error(f'{label}: path escapes the project directory.')
            return None
        if not target.is_file():
            error(f'{label}: file is missing: {name}')
            return None
        digest = item.get('sha256')
        if required and not digest:
            error(f'{label}: approved artifact lacks a checksum.')
        if digest and hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            error(f'{label}: file changed after its checksum was recorded.')
        return target

    def review(record, scope, needs_approval=True):
        if record.get('status') not in STATUSES:
            error(f'{scope}: unknown review status.')
        if record.get('status') == 'approved' and needs_approval and not approval_matches(record, scope):
            error(f'{scope}: no explicit approval record for the current version.')

    exceptions = state.get('exceptions', [])

    def exception(kind, key, value):
        return any(e.get('kind') == kind and e.get(key) == value and e.get('reason')
                   and e.get('user_message') and e.get('recorded_at')
                   for e in exceptions if isinstance(e, dict))

    if state.get('schema_version') != 1: error('Unsupported state schema.')
    if state.get('language') not in ('pt', 'en'): error('Language must be pt or en.')
    if not (root / 'CONTINUITY.md').is_file(): error('CONTINUITY.md is missing.')
    stages = state.get('stages', {})
    expected = [f'{n:02d}' for n in range(1, 10)]
    if set(stages) != set(expected): error('Exactly nine stage records, 01 through 09, are required.')

    for index, stage_id in enumerate(expected):
        stage = stages.get(stage_id, {})
        review(stage, f'stage:{stage_id}', stage_id not in ('05', '07'))
        approved = stage.get('status') == 'approved'
        if approved and not stage.get('version'): error(f'stage:{stage_id}: missing version.')
        if stage.get('status') in ('in_progress', 'awaiting_approval', 'approved'):
            for prior in expected[:index]:
                if stages.get(prior, {}).get('status') != 'approved' and not exception('stage_waiver', 'stage_id', prior):
                    error(f'stage:{stage_id}: earlier stage {prior} has not been approved.')
        artifacts = stage.get('artifacts', [])
        if approved and stage_id not in ('05', '07') and not artifacts:
            error(f'stage:{stage_id}: approved stage has no reviewable artifact.')
        for n, item in enumerate(artifacts):
            artifact(item, f'stage:{stage_id}:artifact:{n}', required=approved)

    segments = state.get('segments', [])
    count = state.get('segment_count')
    planning_done = stages.get('03', {}).get('status') == 'approved'
    if count is not None and (type(count) is not int or count < 1):
        error('Segment count must be a positive integer.')
    if planning_done and (count is None or len(segments) != count):
        error('Approved plan must specify its segment count and every planned segment.')
    ids = [s.get('id') for s in segments]
    if len(set(ids)) != len(ids) or any(not i for i in ids): error('Segment IDs must be unique and nonempty.')
    durations = [s.get('duration_seconds') for s in segments]
    valid_durations = all(type(d) in (int, float) and d > 0 for d in durations)
    if planning_done and (not valid_durations or not segments): error('Every planned segment needs a positive duration.')
    total = state.get('total_duration_seconds')
    if planning_done and (type(total) not in (int, float) or total <= 0): error('Approved plan needs a total duration.')
    elif planning_done and valid_durations and abs(sum(durations) - total) > 0.05:
        error('Total duration does not match the sum of segment durations.')

    previous_out, unique_refs = None, set()
    for s in segments:
        sid = s['id']
        refs = s.get('references', {})
        prod = s.get('production', {})
        review(refs, f'references:{sid}')
        review(prod, f'clip:{sid}')
        ref_approved = refs.get('status') == 'approved'
        clip_approved = prod.get('status') == 'approved'
        if refs.get('status') in ('in_progress', 'awaiting_approval', 'approved'):
            if stages.get('04', {}).get('status') != 'approved' and not exception('stage_waiver', 'stage_id', '04'):
                error(f'{sid}: reference production needs the approved visual guide.')
        if prod.get('status') in ('in_progress', 'awaiting_approval', 'approved'):
            if stages.get('06', {}).get('status') != 'approved' and not exception('stage_waiver', 'stage_id', '06'):
                error(f'{sid}: clip production needs the approved animatic.')
        opening = artifact(refs.get('in'), f'{sid}:IN', required=ref_approved)
        closing = artifact(refs.get('out'), f'{sid}:OUT', required=ref_approved)
        unique_refs.update(p for p in (opening, closing) if p is not None)
        if previous_out and opening and opening != previous_out:
            if exception('boundary', 'segment_id', sid):
                warnings.append(f'{sid}: an explicitly recorded boundary exception is in use.')
            else:
                error(f'{sid}: IN must reuse the same file as the previous OUT.')
        previous_out = closing
        if clip_approved and not ref_approved: error(f'{sid}: approved clip has unapproved references.')
        for field in ('clip', 'actual_first_frame', 'actual_last_frame'):
            artifact(prod.get(field), f'{sid}:{field}', required=clip_approved)
        if clip_approved and not prod.get('continuity_review'):
            error(f'{sid}: approved clip lacks a review of its actual boundary frames.')
        if stages.get('05', {}).get('status') == 'approved' and not ref_approved:
            error(f'{sid}: stage 05 is approved but this pair is not.')
        if stages.get('07', {}).get('status') == 'approved' and not clip_approved:
            error(f'{sid}: stage 07 is approved but this clip is not.')

    if any(stages.get(i, {}).get('status') == 'approved' for i in ('05', '07')) and not segments:
        error('Reference/production stage cannot be approved without segments.')
    if segments and all(s.get('references', {}).get('status') == 'approved' for s in segments):
        if len(unique_refs) != len(segments) + 1:
            warnings.append('Unique reference count differs from N+1; check intentional reuse or recorded exceptions.')

    publication = state.get('publication', {})
    if publication.get('status') not in ('not_published', 'approved_for_publication', 'published'):
        error('Unknown publication status.')
    if publication.get('status') in ('approved_for_publication', 'published'):
        if stages.get('09', {}).get('status') != 'approved': error('Publication requires stage 09 approval.')
        auth = publication.get('authorization') or {}
        if not auth.get('user_message') or not auth.get('recorded_at') or not publication.get('channel'):
            error('Publication needs a recorded user authorisation and a specific channel.')
    if publication.get('status') == 'published' and not publication.get('evidence'):
        error('Published status requires evidence of successful publication.')
    complete = all(stages.get(i, {}).get('status') == 'approved' for i in expected)
    return {
        'consistent': not errors,
        'readiness': 'approved_package' if complete and not errors else 'draft_or_incomplete',
        'publication_status': publication.get('status'),
        'current_stage': next((i for i in expected if stages.get(i, {}).get('status') != 'approved'), None),
        'unique_references_found': len(unique_refs), 'errors': errors, 'warnings': warnings,
        'scope': 'Record/file checks only. Scientific meaning, visual quality and genuine user approval require review.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    create = sub.add_parser('init')
    create.add_argument('directory')
    create.add_argument('--language', choices=('pt', 'en'), required=True)
    create.add_argument('--title', required=True)
    check = sub.add_parser('check')
    check.add_argument('directory')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            print(json.dumps({'created': str(init_project(args.directory, args.language, args.title))}, ensure_ascii=False))
        else:
            report = check_project(args.directory)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0 if report['consistent'] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
