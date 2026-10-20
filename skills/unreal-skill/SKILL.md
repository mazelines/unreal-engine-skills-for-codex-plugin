---
name: unreal-skill
description: Create, revise, or review reusable Unreal Engine workflow skills for Codex, or engine Agent Skills when the connected unrealMCP implementation supports them. Use for SKILL.md authoring, project workflow instructions, or Agent Skill registration. Exclude executing an existing editor workflow and implementing MCP tools.
---

# Author Unreal workflow skills for Codex

Choose the delivery format from the request and installed engine capabilities. Default to a portable Codex skill for workflows meant to guide Codex. An engine Agent Skill is a separate optional implementation, not a requirement for using unrealMCP.

## Choose the target

| Target | Use when | Deliverable |
| --- | --- | --- |
| Codex skill | Reusable source/editor workflow, conventions, build or verification guidance | `<skill-name>/SKILL.md`, relevant references, optional `agents/openai.yaml` |
| Engine Agent Skill | Instructions registered inside an engine with that registry | Supported Python skill class or Agent Skill asset |

Inspect existing guidance and skills first. Extend the existing owner of a workflow rather than introducing a competing copy. For engine registration, discover real schemas; if absent, deliver the Codex form or explain the missing capability without inventing a UAsset type.

## Codex format

Create a lowercase hyphenated folder and matching frontmatter `name` under 64 characters. The `description` should state the task and when to select it, with a boundary from neighboring skills. Store repo skills under `.agents/skills/`; for user installation honor the configured skill root or requested destination. Avoid duplicate names across roots.

```markdown
---
name: unreal-level-review
description: Review this project's Unreal level layout against its traversal and naming rules before a level handoff.
---

Inspect the target map and applicable project rules before making changes.
Read references/level-rules.md for this project's traversal constraints.
Use the connected MCP server's discovered inspection tools and verify findings
against actual actors and transforms. Report object paths with each finding.
```

Write project knowledge or workflow decisions tools cannot readily teach: naming, units, build targets, content ownership, ordering constraints, and observable acceptance criteria. Put substantial conditional procedures in linked references. Keep the skill self-contained; don't require unavailable companion skills.

For MCP use, require capability/schema discovery, establish target project/map, use source tools for code and editor tools for binary assets, and verify mutations with readback. Don't hardcode one server's tool names as universal. A missing editor may block runtime verification while source work remains possible.

For UI metadata, include `interface.display_name`, a 25–64 character `short_description`, and a `default_prompt` mentioning `$skill-name` in `agents/openai.yaml`. Quote strings. Leave automatic selection enabled unless the user requests otherwise. Declare a fixed MCP dependency only when that exact connection is required.

## Engine format

Only for a verified ToolsetRegistry/AgentSkill implementation, read [engine-agent-skills.md](references/engine-agent-skills.md). Its decorators, methods and UAsset types are engine-build-specific examples; confirm them in local source and live schemas. Choose Python for plugin-owned guidance and an asset for project-owned content where supported. Read back registered instructions after reload/save.

## Validate and maintain

Validate frontmatter, referenced files and UI metadata. Review realistic positive and negative discovery requests, an offline-editor case, and expected verification evidence. Run helper scripts in a temporary project before delivery. Report static validation separately from engine execution.

For user-managed skills, follow applicable local/cloud maintenance instructions: reuse a recorded cloud ID or locate an unambiguous name match, preserve visibility, and update all references/assets/metadata with the instructions. Only claim sync after verifying saved cloud contents. If upload is unavailable, preserve the local skill and a complete upload ZIP and state the blocker. Cloud storage does not grant access to a localhost Unreal server.
