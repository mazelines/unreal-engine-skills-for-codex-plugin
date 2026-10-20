# Engine Agent Skill reference

Only use this reference for an engine that actually implements the Agent Skill APIs below. These are separate from Codex SKILL.md folders. Confirm Python symbols and MCP schemas in the installed build before using these examples.

You are authoring an Unreal Engine Agent Skill: a named, reusable bundle of instructions that packages essential knowledge the agent either doesn't know or needs to pay close attention to. A skill can provide general best practices in a domain, guidance on a specific workflow, or a mix of both.

## Principles

A good skill is:

**Novel**: The content should be things the agent doesn't already know or can't learn by using tools. If the agent could figure it out by calling a tool, don't put it in a skill.

**Collegial**: Write like you're briefing a knowledgeable colleague, not authoring documentation. Assume the reader understands Unreal. Give them what they need to act, not a full explanation of how everything works.

**Flexible**: Skills can include conceptual explanations, step-by-step instructions, or a mix. Use whichever form makes the guidance clearest for the task.

**Durable**: Don't embed property names, tool names, or other details that change over time. Skills that reference specific API names break silently when those names change.

**Agnostic**: Don't reference orchestration systems, role names, model names, or anything about how the agent is wired up. Skills should work regardless of the surrounding infrastructure.

**Parsimonious**: Every token costs context. Put them where they matter most and cut anything that isn't essential or evergreen. If a sentence wouldn't be missed, remove it.

## Before You Write

Work through these questions before writing anything.

**1. Does the skill already exist?** Call `ListSkills` via MCP to see all registered skills in the project, then `GetSkills` on anything relevant. If already covered, extend or use the existing skill as appropriate to the request.

**2. Choose the implementation path.** Two paths exist and the choice depends on where the skill lives:

- **Python class**: The right choice when the skill is part of a code plugin. It lives alongside the plugin's Python toolsets, is version-controlled with the plugin, and is registered automatically when the plugin loads.
- **UAsset**: The right choice when the skill is project-specific and doesn't belong in a plugin. Create it directly in the Content Browser using `CreateSkill` via MCP. No code required.

## Structure

Every Unreal skill has two fields.

**Description**: Loaded at discovery time, before the skill's full instructions are read. One or two sentences that clearly describe what the skill covers and when it applies.

**Instructions**: The skill's payload. The actual guidance the agent follows when the skill is active. Apply the principles above: focus on what tools can't teach and cut anything not essential.

The agent discovers and dispatches tools at runtime through the unreal-mcp meta-tools (`list_toolsets`, `describe_toolset`, `call_tool`), so write instructions that assume the agent will find the tools it needs rather than naming a fixed toolset list.

## Python Skills

A Python skill is a `UAgentSkill` subclass defined in a Python file inside a plugin. Use this path when the skill belongs to a code plugin and should be version-controlled with the plugin.

### Authoring

Decorate the class with `@agent_skill` and inherit from `unreal.AgentSkill`. The two fields from the Structure section map to class attributes:

- The class docstring becomes the `Description`. Keep it to one or two sentences.
- `instructions` is a class attribute string containing the guidance loaded when the skill activates.

```python
import unreal

from toolset_registry.agent_skill import agent_skill

_INSTRUCTIONS = (
    'Do X before Y, because Z.\n'
    'Always verify the result after performing the operation.\n'
)

@agent_skill
class MySkill(unreal.AgentSkill):
    """Provides guidance on doing X in Unreal Engine.
    Apply this skill whenever the user wants to accomplish X."""

    instructions = _INSTRUCTIONS
```

### Registration

Skills register themselves on import. Unless directed otherwise, place skill files in a `skills/` subfolder within the plugin's Python package, import each one explicitly in that subfolder's `__init__.py`, and ensure `init_unreal.py` imports the `skills` package.

### Reloading

After editing a Python skill, reload via the supported project mechanism. Only if the helper exists in this engine and Remote Execution is already configured or explicitly requested, use:

```bash
python Engine/Plugins/Experimental/ToolsetRegistry/Content/Python/toolset_registry/tests/reload_remote.py your_plugin
```

## UAsset Skills

A UAsset skill is a `UAgentSkill` instance saved as a Content Browser asset. Use this path for project-specific skills that don't belong in a plugin and require no code.

### Authoring

Use `AgentSkillToolset` via MCP. Start by calling `ListSkills` to see what exists, then either create or update:

**Creating**: Call `CreateSkill` with:
- `FolderPath`: Content Browser folder, e.g. `/Game/Skills/`
- `AssetName`: PascalCase name, e.g. `MyWorkflowSkill`
- `Description`: one or two sentences (see Structure above)
- `Details`: a `FAgentSkillDetails` with `Instructions`

**Updating**: Call `UpdateSkill` with:
- `SkillPath`: full path to the skill, e.g. `/Game/Skills/MyWorkflowSkill.MyWorkflowSkill_C`
- `Description`: revised description
- `Details`: revised `FAgentSkillDetails`

## Reviewing Your Work

Before handing off, verify the skill looks right by calling `GetSkills` on its path. Then read the description and instructions together as the agent will see them:

- **Description**: Does it clearly say when this skill applies? Would an agent reading only the description know whether to activate it for a given task?
- **Instructions**: Do they teach something the agent couldn't learn from the tools? Are they brief enough to be worth the context cost?
