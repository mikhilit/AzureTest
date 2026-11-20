import anthropic

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "list_open_incidents",
        "description": "Return the currently open incidents as a JSON array.",
        "input_schema": {"type": "object", "properties": {}},
    }
]


def run_tool(block):
    if block.name == "list_open_incidents":
        return '[{"id": "INC-201", "summary": "Payment API latency", "severity": "high"}]'
    return f"Unknown tool: {block.name}"


messages = [{"role": "user", "content": "Summarise the open incidents and file a report."}]

while True:
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=4096,
        tools=TOOLS,
        messages=messages,
    )
    if response.stop_reason != "tool_use":
        break
    messages.append({"role": "assistant", "content": response.content})
    tool_results = [
        {"type": "tool_result", "tool_use_id": block.id, "content": run_tool(block)}
        for block in response.content
        if block.type == "tool_use"
    ]
    messages.append({"role": "user", "content": tool_results})