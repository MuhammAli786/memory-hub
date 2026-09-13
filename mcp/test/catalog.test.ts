import { describe, search, type Tool } from "../src/catalog.ts";

const tools: Tool[] = [
  { name: "wiki_search", summary: "Search curated knowledge.", input: { query: "string" } },
  { name: "code_graph_list", summary: "List code graph metadata.", input: {} },
];

if (search(tools, "wiki")[0].name !== "wiki_search") throw new Error("search ranking failed");
if (describe(tools, ["code_graph_list"])[0].name !== "code_graph_list") throw new Error("describe failed");
