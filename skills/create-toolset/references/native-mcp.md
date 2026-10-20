# Native MCP / editor bridge integration

Read this when the installed server exposes individual MCP tools. Use local server code and dependency versions as the source of truth.

## Trace one neighboring command

- Locate the MCP function, type annotations and description that publish its schema.
- Trace requests through transport and editor dispatch. Reuse established timeouts, editor-thread scheduling, and connection ownership.
- Locate handler registration and shutdown cleanup. Add the command through the same lifecycle.
- Trace errors back to the caller. Protocol success may contain an application failure; preserve the server's status/error contract.

## Contract checks

Prefer object paths to display labels; specify units. Validate paths, object lifetime, expected classes, ranges and editor state before writes. Return identifiers and values that support readback. Bound bulk operations by explicit targets.

For queued work, return a job handle with a supported status query or await completion. Distinguish timeout from failure; re-query before repeating mutations. Don't silently retry partially completed bulk edits.

## Test both layers

Test schema serialization and handlers with invalid targets and malformed input. Mock transport tests don't replace an editor round trip. After reload/reconnect, verify the advertised schema and execute a bounded success and failure case in disposable content.
