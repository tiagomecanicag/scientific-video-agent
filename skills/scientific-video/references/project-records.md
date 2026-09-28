# Project records and validation

Keep the project state in the researcher's output folder, never inside the installed skill. The supplied JSON is a neutral template; empty fields mean unknown, not zero or approved. Use the current conversation to interpret user decisions. The record is an audit aid, not an authentication system.

## Files

- `project_state.json`: machine-readable stages, references, clips and decisions.
- `CONTINUITY.md`: concise human-readable summary in the selected language, using the supplied PT or EN template.
- `01_sources/`: supplied paper/data copies when needed; preserve originals.
- `02_script/`: scientific interpretation, narrative, script and visual guide.
- `03_references/`: approved and revised IN/OUT images; reuse a single file at shared boundaries.
- `04_animatic/`: previews and timing notes.
- `05_segments/`: individual clips and extracted frames.
- `06_edit/`: editing project and supporting materials.
- `07_export/`: assembled films and review versions.
- `08_publication/`: approved public package, separate from internal records.
- `09_documentation/`: decisions, reviews and handover notes.

Use relative artifact paths within the project. Copy an external approved boundary image into the project once and record its source; both neighbouring segments then reference that same copy. Do not copy source papers or private project records into the distributable agent package.

## Stage records

The nine stage IDs are `01` through `09`. Each has `status`, `version`, `artifacts`, `approvals` and `notes`. Statuses: `pending`, `in_progress`, `awaiting_approval`, `approved`, `needs_revision`.

When delivering a result, set its version and `awaiting_approval`. Record artifacts as objects with `path` and `sha256`; compute hashes from actual bytes. Never invent a checksum or a file that has not been created. The SHA-256 records allow later checks to detect changes to the reviewed files.

After explicit approval, append an approval object and set `approved`:

```json
{
  "decision": "approved",
  "version": "v1",
  "scope": "stage:01",
  "user_message": "The user's actual approval wording",
  "recorded_at": "ISO 8601 timestamp",
  "reviewer": null
}
```

Use `stage:NN` for whole-stage reviews, `references:T01` for a reference pair, and `clip:T01` for a clip. Record only wording actually received, not the example above. Reviewer identity is optional; do not infer it from paper authors. One approval can cover an explicitly identified batch, but each affected record must point to that actual decision and version.

Stage 05 is approved only after every planned segment's `references` record is approved; stage 07 only after every `production` record is approved. After the last unit is approved, the stage may be closed from those existing approvals; no redundant extra approval is required. Those two stage records can omit a separate stage approval if all their units pass review.

## Segment records

After stage 03 is approved, set `segment_count`, `total_duration_seconds` and create the planned `segments` array using [../assets/segment.template.json](../assets/segment.template.json). Use stable IDs such as `T01`. Each segment has `id`, positive `duration_seconds`, `role`, `narration`, `references` and `production`.

Reference records contain the standard status/version/approvals fields plus `in` and `out`, each an artifact object. Production records contain status/version/approvals plus `clip`, `actual_first_frame`, `actual_last_frame`, and `continuity_review` (a short description of what was checked and any approved deviation). Keep the actual frame evidence instead of claiming the planned OUT was the observed frame.

Shared boundaries use identical paths, not merely visually similar images. If the researcher explicitly approves an exception, record it in `exceptions` with `kind: "boundary"`, `segment_id` for the incoming segment, `reason`, `user_message` and `recorded_at`. A `stage_waiver` exception uses `stage_id` instead. Such exceptions document a real user decision; they must never be created to make a failed check pass.

## Revisions and resuming

Preserve previous versions and approvals in the records. Change the current version and status of revised work to `needs_revision` or `in_progress`; old approval entries remain historical and do not approve the new version. Mark dependent stages/segments for review. A change to an OUT normally affects the next IN, the animatic and both adjacent clips.

On resume, read both records, check referenced files and their hashes, and use the most recent valid user-approved version. Resolve genuine conflicts with the user while progressing on independent authorised work. If the selected language changes, update the human-facing log; keep scientific content, IDs and approvals.

Run `python scripts/project.py check <project-directory>` using the script path relative to this skill. Exit 0 means the current records are consistent, not that the project is finished. The report explicitly distinguishes a consistent draft from an approved final package. The checker cannot prove that a user message is authentic, that a chart is accurate or that a video looks correct; those require actual conversation evidence and scientific/visual review.
