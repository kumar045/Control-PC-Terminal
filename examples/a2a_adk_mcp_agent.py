#!/usr/bin/env python3
"""A2A + ADK + MCP custom agent template for Control-Terminal.

This file is intentionally minimal and framework-agnostic so users can see the
shape of an interactive custom agent process.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable


@dataclass
class MCPServer:
    """Represents one MCP server endpoint the agent can talk to."""

    name: str
    url: str


@dataclass
class AgentConfig:
    """Runtime configuration for the custom agent."""

    agent_name: str = "terminal_orchestrator"
    mcp_servers: list[MCPServer] = field(
        default_factory=lambda: [
            MCPServer(name="filesystem", url="http://localhost:3001"),
            MCPServer(name="docs", url="http://localhost:3002"),
        ]
    )


class A2AAdapter:
    """Stub adapter for A2A message ingress/egress."""

    def receive(self, user_text: str) -> dict[str, str]:
        return {"role": "user", "content": user_text.strip()}

    def send(self, text: str) -> None:
        print(text, flush=True)


class MCPBridge:
    """Stub MCP bridge.

    Replace this with real MCP client calls (tool listing, resource reads, etc.).
    """

    def __init__(self, servers: Iterable[MCPServer]) -> None:
        self.servers = list(servers)

    def summarize_servers(self) -> str:
        parts = [f"{server.name}={server.url}" for server in self.servers]
        return ", ".join(parts)


class ADKOrchestrator:
    """Stub ADK orchestrator.

    Replace `run` with your ADK workflow graph/planner.
    """

    def __init__(self, config: AgentConfig, mcp: MCPBridge) -> None:
        self.config = config
        self.mcp = mcp

    def run(self, message: dict[str, str]) -> str:
        content = message["content"]
        if content == "/status":
            return (
                f"agent={self.config.agent_name} | "
                f"time={datetime.utcnow().isoformat()}Z | "
                f"mcp=[{self.mcp.summarize_servers()}]"
            )

        return (
            "[A2A→ADK→MCP template]\n"
            f"received: {content}\n"
            "next: replace ADKOrchestrator.run() with your real workflow."
        )


def main() -> None:
    config = AgentConfig()
    a2a = A2AAdapter()
    mcp = MCPBridge(config.mcp_servers)
    adk = ADKOrchestrator(config=config, mcp=mcp)

    print("Custom agent started (A2A + ADK + MCP template).", flush=True)
    print("Type '/status' to check configuration, or 'exit' to quit.", flush=True)

    while True:
        try:
            user_input = input("agent> ")
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit cleanly.", flush=True)
            continue

        if user_input.strip().lower() in {"exit", "quit"}:
            print("Shutting down custom agent.", flush=True)
            break

        if not user_input.strip():
            continue

        message = a2a.receive(user_input)
        response = adk.run(message)
        a2a.send(response)


if __name__ == "__main__":
    main()
  
