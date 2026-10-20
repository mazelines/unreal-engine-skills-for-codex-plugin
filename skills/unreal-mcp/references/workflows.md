# Unreal source and editor workflows

## Source context and builds

Find the `.uproject` engine association, relevant `.uplugin`, `.Build.cs`, and `*.Target.cs` before selecting APIs or build commands. An installed engine and a source engine have different layouts. Use existing project scripts/CI as the first source for target, platform and configuration. Preserve source-control changes and generated code ownership.

Follow nearby UObject lifetime, reflection and module conventions. Keep the generated header last among includes in reflected headers. Add module dependencies where actually needed; editor-only APIs belong in editor modules or appropriate guards. Do not hand-edit UHT output, `Intermediate/`, or `Binaries/` as a source fix.

### Live Coding or full build

- A supported implementation-only C++ edit can use Live Coding if enabled and the server exposes a compile tool. Discover its actual signature and wait for completed diagnostics.
- Reflected class/property/function declarations, constructors/defaults, module layout and generated-code changes can require a full editor-target build and restart. Assess the engine/build's limitations; don't promise safe reinstancing for every change.
- Without a compile tool, use the project's build script from the shell with actual paths. Don't issue a competing full build while Live Coding is active. Arrange editor closure/restart only when needed within the task, preserving unsaved work.
- A build success doesn't prove that the loaded editor has the new code. Verify the loaded class/property or behavior after compile/restart.

Illustrative Windows PowerShell command (replace every path/target with verified values):

```powershell
& "D:/UE/Engine/Build/BatchFiles/Build.bat" MyGameEditor Win64 Development "D:/Projects/MyGame/MyGame.uproject" -WaitMutex
```

Use the platform's real build script on Linux/macOS; do not run this Windows example there. Read diagnostics and the process exit code before runtime tests.

## Editor content

| Work | Inspection before change | Verification after change |
| --- | --- | --- |
| Actors/levels | Map, world, actor paths, units and transforms | Re-query transforms/counts, save affected map, screenshot if visual |
| Blueprints/widgets | Parent class, graph, variable types, pin directions | Compile diagnostics, graph/property readback, relevant interaction |
| Materials/Niagara | Existing asset graph, parameters and engine support | Compile state, parameter readback and visual preview |
| Sequencer/animation | Sequence path, bindings, frame rate/range, rig/skeleton | Binding/key readback and a supported preview |
| Gameplay/GAS | Ownership, replication/net role, input and dependencies | Targeted automation or PIE scenario with actual runtime evidence |

These domains are candidates for capability discovery, not a promise that every MCP server supports them. If a tool is missing, inspect supported editor Python/native APIs or implement an explicit tool extension within scope. Don't silently substitute a different server or broad arbitrary script execution.

## Tests and evidence

Discover automation tools and schemas if present. List/filter the intended tests, start them, wait for completion and inspect detailed results. A returned job handle is not a passing test. After Python reload, use supported rediscovery if new tests are absent.

For headless automation, prefer the project's existing runner. A common UE pattern uses `-ExecCmds="Automation RunTests <filter>"`, `-TestExit="Automation Test Queue Empty"`, and a report path, but verify these against the engine version and project runner. Do not append an immediate `quit`. Use `-NullRHI` only for tests that don't require rendering. Inspect completed reports and logs as well as process exit status.

If no Unreal runtime is reachable, validate source and static structure where possible and identify the remaining compile/editor/gameplay checks. Never label a source diff or screenshot as a passed engine automation test.
