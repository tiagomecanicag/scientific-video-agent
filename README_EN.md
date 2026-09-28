# Scientific Video · PT / EN

A science communication agent based on the bilingual “From Research Paper to Scientific Video” prompt kit. Version 0.1.0, local pilot.

## Getting started

After installing the plugin, open a new Codex conversation. Select **Scientific Video · PT / EN**, attach the paper and send:

> Use $scientific-video to turn this paper into a science communication video in English. Guide me through the nine stages with my approval at each checkpoint and keep a project record. Begin with the scientific interpretation of the paper.

Specify where to save the new project. The agent should reuse information you have already supplied rather than ask the same questions again. To resume later, identify the project folder and ask the agent to read `project_state.json` and `CONTINUITY.md`.

The skill identifier is `scientific-video`; the plugin identifier is `scientific-video-agent`. Some interfaces display the plugin name as a prefix to the skill. If the mention is not recognised, select the skill from the interface menu.

## The nine stages

1. Scientific understanding of the paper.
2. Protagonist, audience and narrative.
3. Segment count, script and running time.
4. Visual language and identity.
5. Two images and approval for each segment.
6. Animatic and narrative testing.
7. Production and approval of each segment.
8. Final assembly and review.
9. Communication package and publication approval.

Respond with **Approved**, **Revise: ...** or **Return to stage: ...**, specifying the segment and version when several items are under review. The agent presents the result before requesting approval. Stages 05 and 07 repeat for each segment. Approval of the final pair or clip can close the corresponding stage without asking for the same approval again.

## Continuity and scientific fidelity

Use 1080 × 1920 pixels (width × height), portrait 9:16, as the main recommendation and default format from the start. Present this default for review; change it only at the user’s explicit request. Do not automatically choose another format because of the channel, references or tool limitations.

Each segment has IN and OUT references. The approved OUT is the same file used as the next IN. For N consecutive segments, the plan contains N+1 unique images before revisions and approved exceptions. Segment count depends on the paper; 19 is not a mandatory default.

The first segment has a striking opening connected to the protagonist. The final segment partially dims the scene and rolls the credits upwards while keeping the protagonist visible. Credits use verified information.

The agent must distinguish real data from visual metaphors. Numbers, curves, institutions and conclusions must not be fabricated. Changes to approved materials require an identified revision.

## What is included

A workflow skill, nine prompts in each language, shared rules, record templates and a helper for initialising project folders and checking record consistency. The helper uses Python 3 and the standard library; if Python is unavailable, the agent can maintain the same records using the available file tools.

Image, video, audio and editing tools depend on each researcher's environment. This package does not include a subscription, credits or a video generator. If a tool is unavailable, the agent prepares the production materials and identifies what is still pending.

Approval controls consist of workflow instructions and records. Automated checks detect inconsistencies in versions, files and sequence; they do not independently authenticate an approval or establish scientific correctness. These still require researcher review and inspection of the outputs.

## Sharing without GitHub

Send colleagues the agent ZIP. It contains only the agent and its documentation, not the paper or videos from the original project. Recipients should extract it into their own folder and install the local plugin in a compatible environment.

In Codex, a colleague can use the plugin creation skill with this instruction, attaching or identifying the extracted folder:

> Use $plugin-creator to register and install the local scientific-video-agent plugin from this folder. Preserve its existing instructions and files; do not recreate the agent. Then verify installation and explain how to start it in a new conversation.

Alternatively, without installation, in an environment that can read local files, point to `skills/scientific-video/SKILL.md` and ask the assistant to follow that workflow and read the references for the chosen language. This loads instructions into the conversation; it does not install a plugin.

## Status of this version

The package passes the skill and plugin validators. The helper has been checked with 14 synthetic record and file tests. This is not an end-to-end test of a new paper through to a final video. The first use with another paper is the recommended pilot for evaluating the narrative, visual production and researcher experience.

Keep each paper's project records outside the plugin folder. Share only the materials you intend to distribute; installing the agent does not publish the project.
