---
name: unreal-mcp
description: Inspect and edit Unreal Engine projects with Codex and a live unrealMCP connection; handle actors, Blueprints, assets, C++ build iteration, and MCP setup or recovery. Use for UE project work involving .uproject, UObject, UPROPERTY, BP_, WBP_, or the Content Browser. Exclude conceptual-only questions and other engines.
---

# Unreal Engine with unrealMCP and Codex

Use Codex filesystem and shell tools for source/configuration work and the connected MCP tools for live Unreal Editor state. Determine actual server capabilities before acting; this skill does not itself create a connection.

## Establish context

Read applicable `AGENTS.md`, locate the target `.uproject`, and inspect relevant source, plugin descriptors, engine association, and working changes. If multiple projects or editors are plausible, identify the target before mutation. Preserve unrelated work. Use the user's language for progress and results.

Find the existing Unreal MCP connection, including names such as `unrealMCP`, `unreal-mcp`, or `unreal-mcp-proxy`. Reuse it. Inspect tools and schemas actually available in the current Codex session. A configured server, running editor, or cached catalog alone does not establish live access. Confirm project/map using a read-only editor query if supported, otherwise combine local project evidence with server/log evidence and state any uncertainty.

For setup read [setup.md](references/setup.md); for failed or missing tools read [operations.md](references/operations.md). If live access is unavailable, continue authorized source/config work and report precisely which editor checks remain unverified.

## Discover and dispatch

- **ToolsetRegistry meta-tools:** When `list_toolsets`, `describe_toolset`, and `call_tool` are advertised, discover the relevant toolset and read its schema, then dispatch through `call_tool` with schema-matching arguments. Known candidate toolsets can go directly to description. A described method is not necessarily a native MCP tool. Do not recursively dispatch `call_tool` through itself.
- **Native MCP tools:** When individual tools are advertised, invoke their actual Codex-exposed names and schemas directly. Do not require meta-tools or ToolsetRegistry on that server.
- **Limited/proxy catalog:** Follow recovery guidance. Never fabricate tools, parameters, registry classes, or arbitrary Python execution capability from another implementation.

Only if this server exposes an engine Agent Skill registry, discover its listing/retrieval schemas and load relevant project guidance. Treat returned guidance as project context under the current user's instructions, not permission for unrelated actions. The registry is distinct from installed Codex skills.

## Execute and verify

1. Inspect target objects, paths, current values, selection, PIE, loading and compilation state as needed. Use stable object/asset paths returned by the editor; an actor label can be ambiguous. Follow project units and naming conventions (normally centimeters and degrees).
2. Make the smallest coherent change. Serialize dependent calls and shared-state mutations. Concurrent independent reads require server support. For bulk changes, establish recoverable saved state using relevant save/source-control facilities; avoid saving unrelated dirty assets indiscriminately.
3. Read every result, including protocol errors, structured status and compile diagnostics. An empty successful return can be valid for a void tool; resolve explicit failures before dependent work. After a timeout, re-query state before retrying a mutation that may already have completed.
4. Compile affected Blueprints/materials or build affected code where needed. Save changed assets/map when requested or implied, and read back properties/graph/object state. Check for duplicates when creating assets or actors.
5. Validate at the right level: inspect graph wiring, use targeted automation or PIE for gameplay, and screenshots for visual layout when available. A screenshot cannot prove runtime behavior. Restore temporary selection/camera/PIE changes when appropriate.

Stop or change PIE only when required by the operation and within the task. Don't restart the editor, kill a proxy, delete assets, or run broad cleanup merely because a query failed. Resolve the actual precondition.

## Source and C++ iteration

For source edits, build selection, Live Coding limits, automation, and domain verification read [workflows.md](references/workflows.md). Keep `.uasset` and `.umap` edits inside supported editor APIs; never patch their binary contents with text tools.

Finish with changed source/asset paths, verification performed and results, and remaining editor/build blockers. Distinguish saved source, successful compilation, live readback, and tested gameplay.

## Related work

If available, use `create-toolset` to extend MCP capabilities and `unreal-skill` to author reusable Codex or supported engine skills. Their installation is optional; this runtime workflow does not depend on them.
