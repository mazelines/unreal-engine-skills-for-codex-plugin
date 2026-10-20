# MCP operation and recovery

Start with the configured implementation, transport and actual error. Avoid treating all missing tools as a stopped editor.

| Symptom | Check and next action |
| --- | --- |
| No Unreal tools in Codex | Inspect existing connection names, enabled state and endpoint. A configured connection may not have initialized in this session. Refresh/reconnect or start a new session if supported. |
| Meta-tools absent | Inspect native MCP tools. An independent bridge or full-catalog server may have no ToolsetRegistry meta-tools. |
| Connection refused | Check actual server process, endpoint ownership, editor plugin/startup log, and bridge process if used. Don't assume every editor serves port 8000. |
| Tools listed but calls fail | A proxy can expose cached schemas. Confirm live reachability with a read-only editor call and inspect stderr/startup logs. |
| Tool or plugin missing | Inspect plugin descriptors and this engine's source. Enable/refresh the supported implementation within the requested scope. Don't add Epic-only plugins to another server. |
| Calls stall | Check loading, compilation, PIE and modal UI. Wait for actual completion; after timeout, read state before retrying a mutation. |
| New C++/Python tools absent | Verify successful compile/reload and registration, then refresh server catalog and client connection. Source edits alone don't update the running process. |
| Docked context empty | Some integrations require an embedded editor tab. A standalone Codex session may have none; use explicit project/asset queries instead. |
| Concurrent writes conflict | Serialize dependent edits on the same world/assets. One editor has shared state even when agents use separate code worktrees. |

## Epic-specific console operations

Only use these when present in the installed engine source/help:

| Command | Purpose |
| --- | --- |
| `ModelContextProtocol.StartServer [port]` | Start the editor HTTP server |
| `ModelContextProtocol.StopServer` | Stop that server when a restart is actually needed |
| `ModelContextProtocol.RefreshTools` | Refresh registered toolsets |
| `ModelContextProtocol.GenerateClientConfig Codex` | Generate Codex configuration where supported |

In compatible builds, `bEnableToolSearch=True` in the ModelContextProtocol settings exposes `list_toolsets`, `describe_toolset`, `call_tool`. When false, native tools can be exposed individually. Discover the active mode rather than changing it to match assumed tool names.

## Proxy recovery

The optional Epic proxy may remain initialized while the editor is offline. Its `unreal_mcp_status`, when available, reports proxy session state; it is not a live editor probe. Cached tools are similarly insufficient.

With no cached catalog, a proxy may initially expose only status. After recovery it can send `notifications/tools/list_changed`. If Codex retains an old catalog, use supported reconnect/reload or a new session after verifying that upstream Unreal is reachable. Killing the proxy closes its STDIO transport; launching an unrelated proxy won't repair that client connection. Avoid killing active processes as a routine refresh.

If multiple editors are running, identify the process owning the configured port and correlate its project and log. Preserve the existing connection configuration; a second server name can hide the original targeting error.

## Evidence to report

Record the server name and non-secret endpoint, target project/map evidence, failing operation and error, recovery attempted, and the final read-only query result. Distinguish configured, connected, catalog visible, and editor reachable. Never claim successful writes or tests on the strength of a cached schema.
