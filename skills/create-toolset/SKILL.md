---
name: create-toolset
description: Add or extend Unreal Engine MCP tools for Codex, using the project's existing unrealMCP server or Epic ToolsetRegistry C++/Python implementation. Use for new MCP commands, tool schemas, registration, or toolset methods. Exclude using existing tools, generic code edits, and workflow skill authoring.
---

# Extend Unreal MCP capabilities

Inspect the installed server and editor plugin before choosing an implementation. `unrealMCP` is a connection name, not a guarantee of Epic ToolsetRegistry APIs.

## Find the extension point

1. Read applicable `AGENTS.md`, MCP configuration and nearby implementations. Discover live tools if available. Search existing functionality before adding another command.
2. Follow the architecture: native MCP Python registrations and editor handlers for a bridge server, or reflected toolsets for a verified ToolsetRegistry engine. Don't install an unrelated server or change transport to add a tool.
3. Define a minimal contract: stable object/asset identifiers, units, preconditions (PIE, loading, compilation), return data and errors. Reuse generic property/asset operations. Prefer neighboring conventions over imposing another implementation's rules.
4. Choose Python if the required editor API is exposed and the project uses Python; use C++ for missing reflection access or native operations. Follow a specified language; resolve routine choices from existing architecture. Explain a material missing API before expanding engine scope.

## Implement

For **ToolsetRegistry**, read [toolset-registry.md](references/toolset-registry.md) for preserved C++/Python conventions, async results, converters, registration and tests. Confirm names and availability against this engine's source. Its static-method, typed-return and script-error rules apply to that implementation.

For a **native MCP/bridge server**, inspect an adjacent tool end to end: MCP decorator/schema, transport serialization, editor-thread dispatch, handler, startup/shutdown, and response decoding. Add the capability at the same layers. Read [native-mcp.md](references/native-mcp.md) for integration checks. JSON messages or structured result envelopes may be this server's legitimate contract; don't replace them with ToolsetRegistry types.

Keep UObject/asset mutation on the appropriate editor/game thread. Validate objects and inputs before side effects. Use transactions, dirty flags and saves according to surrounding code. Async success means completion, not merely queueing. Include supported cancellation or timeout behavior for long operations.

## Validate the contract

Test success and meaningful failure cases: missing target, invalid input, unsupported editor state, and retry/idempotency where relevant. Assert resulting state and transport-visible errors. Use isolated test content and avoid broad cleanup of user assets.

Build the affected module with the actual editor target. Use Live Coding only for supported changes; reflected declarations, generated code and module layout may require a full build/restart. Reload Python using the project's supported mechanism, then refresh/reconnect the catalog if necessary. Don't enable remote execution just to reload if an existing path works.

Run targeted automation and a real MCP round trip when available. Discover test schemas and wait for completed results. For command-line automation, use proven completion flags and inspect reports; don't append an immediate `quit` that may terminate queued tests early. If no editor/build is available, deliver source and tests with that limit stated.

Finish with changed files, tool name/schema, registration/reload steps, tests/build results, and remaining runtime checks.
