import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { describe, search, type Tool } from "./catalog.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const catalog = JSON.parse(readFileSync(join(root, "contracts/mcp-tools.json"), "utf8")) as { tools: Tool[] };
const server = new Server({ name: "second-brain-catalog", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    { name: "search", description: "Find memory and knowledge operations by keyword.", inputSchema: { type: "object", properties: { query: { type: "string" }, limit: { type: "integer" } }, required: ["query"] } },
    { name: "describe", description: "Describe selected catalog operations.", inputSchema: { type: "object", properties: { names: { type: "array", items: { type: "string" } } }, required: ["names"] } }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const args = request.params.arguments as { query?: string; limit?: number; names?: string[] };
    const result = request.params.name === "search"
      ? search(catalog.tools, args.query ?? "", args.limit)
      : request.params.name === "describe"
        ? describe(catalog.tools, args.names ?? [])
        : (() => { throw new Error("unknown tool"); })();
    return { content: [{ type: "text", text: JSON.stringify(result) }] };
  } catch (error) {
    return { content: [{ type: "text", text: error instanceof Error ? error.message : "catalog error" }], isError: true };
  }
});

await server.connect(new StdioServerTransport());
