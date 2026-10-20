# Unreal Engine project guidance for Codex

Merge relevant instructions into the project's existing AGENTS.md.

- Locate the target .uproject and engine version before choosing APIs or build commands.
- Use the unreal-mcp skill, when installed, for live editor work and source/build iteration.
- Reuse the configured unrealMCP connection and discover actual tools and schemas.
- Use filesystem tools for source/config; supported editor APIs for .uasset and .umap changes.
- Follow existing UObject ownership, reflection, module dependencies and generated-header conventions.
- Serialize dependent mutations, inspect results, compile as needed, save affected content, and read back state.
- Preserve unrelated changes and dirty assets. Establish a recovery point for broad edits.
- Report separately what was edited, built, saved and tested. If the editor is unavailable, continue source work and state which live checks remain.
