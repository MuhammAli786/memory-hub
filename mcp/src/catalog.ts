export type Tool = { name: string; summary: string; input: Record<string, unknown> };

const terms = (value: string) => value.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);

export function search(tools: Tool[], query: string, limit = 8) {
  const wanted = terms(query);
  return tools
    .map((tool) => ({ tool, score: wanted.reduce((score, word) => score + (terms(`${tool.name} ${tool.summary}`).includes(word) ? 1 : 0), 0) }))
    .filter(({ score }) => score > 0 || wanted.length === 0)
    .sort((left, right) => right.score - left.score || left.tool.name.localeCompare(right.tool.name))
    .slice(0, Math.max(1, Math.min(limit, 20)))
    .map(({ tool }) => ({ name: tool.name, summary: tool.summary }));
}

export function describe(tools: Tool[], names: string[]) {
  const indexed = new Map(tools.map((tool) => [tool.name, tool]));
  return names.map((name) => {
    const tool = indexed.get(name);
    if (!tool) throw new Error(`unknown tool: ${name}`);
    return { name: tool.name, summary: tool.summary, input: tool.input };
  });
}
