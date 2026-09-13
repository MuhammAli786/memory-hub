# MCP Catalog

This package provides a usable, local MCP catalog for Claude and Codex. It has no upstream connection code. It lets an agent discover the vocabulary and schemas it should expect from a private memory integration without embedding private implementation configuration in the public repository.

```sh
pnpm install
pnpm build
node dist/server.js
```

The exposed tools are:

- `search`: rank catalog entries by a natural-language query.
- `describe`: return the selected entry's input schema and safety mode.

Use `.codex/config.template.toml` for Codex registration. Claude can register the same standard-input server in its local MCP settings.
