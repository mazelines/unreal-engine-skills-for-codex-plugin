# Connect unrealMCP to Codex

Read this for first-time setup or connection changes. First inspect the existing connection and installed implementation. A connection named `unrealMCP` may be Epic's HTTP server, an independent UnrealMCP bridge, or another implementation.

## Codex configuration

Use `codex mcp list` and `codex mcp get <existing-name>` to inspect configuration. Reuse existing names and preserve unrelated settings, credentials and policies. Codex reads user `~/.codex/config.toml` and trusted-project `.codex/config.toml`; an upstream Claude `.mcp.json` is not a standalone Codex configuration.

For a verified Streamable HTTP endpoint, the CLI can add a user connection:

```powershell
codex mcp add unrealMCP --url http://127.0.0.1:8000/mcp
```

For project scope, merge only the relevant table into `.codex/config.toml`:

```toml
[mcp_servers.unrealMCP]
url = "http://127.0.0.1:8000/mcp"
startup_timeout_sec = 20
tool_timeout_sec = 120
```

The address above is an example. Use the actual server port/path. Adjust timeouts for observed startup/compile duration, not to mask a broken connection. Don't enable permission bypass settings as a setup step.

If the installed bridge is a STDIO Python program, translate its documented command/args into TOML. For a bridge whose real entry point is `Python/unreal_mcp_server.py` via `uv`, an example is:

```toml
[mcp_servers.unrealMCP]
command = "uv"
args = ["--directory", "D:/Tools/unreal-mcp/Python", "run", "unreal_mcp_server.py"]
startup_timeout_sec = 20
tool_timeout_sec = 120
```

Install dependencies and the matching editor plugin according to that implementation. A bridge's editor TCP port is not necessarily an HTTP MCP endpoint. STDIO servers must reserve stdout for protocol output. Keep local endpoints on loopback unless the user explicitly requests a secured remote arrangement.

## Epic ModelContextProtocol / ToolsetRegistry builds

These instructions apply only after checking that this engine includes the relevant plugins and settings in source/descriptors. Do not add nonexistent plugins to a launcher project or an independent UnrealMCP installation.

In a build with `ModelContextProtocol` and `AllToolsets`, enable the server and either the toolset aggregator or required individual toolset plugins. Preserve the target `.uproject` JSON and existing plugin entries. Enable within the user's setup request; if multiple projects exist, identify the target before editing.

```json
{"Plugins": [
  {"Name": "ModelContextProtocol", "Enabled": true},
  {"Name": "AllToolsets", "Enabled": true}
]}
```

Use the editor console's supported `ModelContextProtocol.StartServer [port]`. In compatible builds, user settings in `<Project>/Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini` include:

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
ServerPortNumber=8000
ServerUrlPath=/mcp
```

Do not create a second INI section when merging. Check actual settings in the local build. The original engine workflow also supports `-ModelContextProtocolStartServer` and an optional port flag where implemented.

If supported, `ModelContextProtocol.GenerateClientConfig Codex` generates Codex TOML. The original source workflow writes at the workspace root for source builds and next to the `.uproject` for installed builds; confirm the actual output log. Some writers refuse to overwrite existing `.codex/config.toml`. Merge the endpoint manually when it already exists. Do not generate a Claude config and expect standalone Codex to read it.

## Optional Epic proxy

Only use a proxy present in this engine's `Engine/Plugins/Experimental/ModelContextProtocol/Extras/Proxy`. Read its bundled README and `--help` for the supported upstream argument and transport. Platform binaries may exist under `Bin/Win64`, `Bin/Mac`, `Bin/Linux` or `Bin/LinuxArm64`.

Do not run a `.mcp.json` installer against a Codex TOML file. If that build's installer only edits Claude-style JSON, it does not configure Codex. Configure a Codex STDIO `command` and `args` only after verifying how that executable receives the upstream URL/config; don't invent flags. If unsupported, retain direct HTTP. Keep one connection rather than proxy plus duplicate direct registration.

## Verify

Refresh/reconnect the MCP connection using the installed client controls, or start a new Codex session if required. `codex mcp list` and `/mcp` in the CLI TUI show configuration/session information; they do not prove editor reachability. Confirm server startup logs, available schemas, and a successful read-only editor query that identifies the intended project/map.

If the current Codex session does not expose tools even though the CLI configuration exists, don't simulate editor results. See [operations.md](operations.md).

Official references: [Codex MCP](https://developers.openai.com/codex/mcp/) and [Codex skills](https://developers.openai.com/codex/skills/). For independent bridges, use the installed repository's documentation, for example [unreal-mcp](https://github.com/chongdashu/unreal-mcp).
