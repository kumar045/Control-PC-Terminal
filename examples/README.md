# Examples

This folder contains starter examples for building a custom agent that can be launched by `control-terminal`.

## A2A + ADK + MCP starter

Use `a2a_adk_mcp_agent.py` as a reference structure when creating your own agent.

### What the example demonstrates

- A **single launcher command** that starts policy/research/provider/healthcare agents together.
- A clear split of concerns:
  - **A2A adapter** for receiving/sending messages.
  - **ADK orchestration** for task routing/execution.
  - **MCP client bridge** for tools/context from MCP servers.
- Persistent stdin/stdout loop that keeps running to process the next prompt (interactive terminal or tmux-driven input).

### Run the example directly

```bash
python3 examples/a2a_adk_mcp_agent.py
```

This process stays alive and reads prompts from stdin.

```bash
# interactive terminal mode
python3 examples/a2a_adk_mcp_agent.py

# tmux/automation can send newline-terminated prompts to stdin
# and capture stdout replies from the same long-running process
```

### Register as a preconfigured Control-Terminal agent

Add this line to your `~/.control-terminal/custom-agents.conf`:

```text
a2a-adk-mcp-example|python3 /absolute/path/to/Control-PC-Terminal/examples/a2a_adk_mcp_agent.py
```

Now select **preconfigured custom agent** in `control-terminal` and choose `a2a-adk-mcp-example`.

### Automatic skills attachment in examples

The example agents now auto-attach role skills loaded from `examples/skills/*/SKILL.md` (via `examples/skill_registry.py`) at startup:

- `a2a_policy_agent.py` -> `policy` skills
- `a2a_research_agent.py` -> `research` skills
- `a2a_provider_agent.py` -> `provider` skills
- `a2a_healthcare_agent.py` -> `healthcare` skills

This behavior is intentionally static in the examples (no env/CLI override path).
Each agent uses both SKILL frontmatter metadata and the short guidance body from each `SKILL.md` file.

## Notes

- This is a **template/example** and intentionally uses lightweight placeholder logic so you can replace pieces with your real SDK integrations.
- Update MCP server list, ADK workflow, and A2A transport based on your stack.
