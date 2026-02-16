# Examples

This folder contains starter examples for building a custom agent that can be launched by `control-terminal`.

## A2A + ADK + MCP starter

Use `a2a_adk_mcp_agent.py` as a reference structure when creating your own agent.

### What the example demonstrates

- A **single terminal agent process** that stays alive and reads prompts continuously.
- A clear split of concerns:
  - **A2A adapter** for receiving/sending messages.
  - **ADK orchestration** for task routing/execution.
  - **MCP client bridge** for tools/context from MCP servers.
- A simple `/status` command and graceful shutdown flow.

### Run the example directly

```bash
python3 examples/a2a_adk_mcp_agent.py
```

Then type prompts in the terminal.

### Register as a preconfigured Control-Terminal agent

Add this line to your `~/.control-terminal/custom-agents.conf`:

```text
a2a-adk-mcp-example|python3 /absolute/path/to/Control-PC-Terminal/examples/a2a_adk_mcp_agent.py
```

Now select **preconfigured custom agent** in `control-terminal` and choose `a2a-adk-mcp-example`.

## Notes

- This is a **template/example** and intentionally uses lightweight placeholder logic so you can replace pieces with your real SDK integrations.
- Update MCP server list, ADK workflow, and A2A transport based on your stack.
- 
