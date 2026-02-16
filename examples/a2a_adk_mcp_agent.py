#!/usr/bin/env python3
"""Single-command launcher for the healthcare A2A demo stack.

Run this file once to start the policy, research, provider, and healthcare
agents. The process then stays alive, reading prompts from stdin and writing
responses to stdout.
"""

from __future__ import annotations

import asyncio
import os
import signal
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from beeai_framework.adapters.a2a.agents import A2AAgent
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.middleware.trajectory import EventMeta, GlobalTrajectoryMiddleware

from helpers import setup_env


@dataclass(frozen=True)
class ManagedAgent:
    """Metadata needed to run and monitor one agent process."""

    name: str
    script: str
    port_env: str


AGENTS = [
    ManagedAgent("Policy Agent", "a2a_policy_agent.py", "POLICY_AGENT_PORT"),
    ManagedAgent("Research Agent", "a2a_research_agent.py", "RESEARCH_AGENT_PORT"),
    ManagedAgent("Provider Agent", "a2a_provider_agent.py", "PROVIDER_AGENT_PORT"),
    ManagedAgent(
        "Healthcare Concierge Agent",
        "a2a_healthcare_agent.py",
        "HEALTHCARE_AGENT_PORT",
    ),
]

DEFAULT_PORTS = {
    "POLICY_AGENT_PORT": 9999,
    "RESEARCH_AGENT_PORT": 9998,
    "PROVIDER_AGENT_PORT": 9997,
    "HEALTHCARE_AGENT_PORT": 9996,
}


class ConciseGlobalTrajectoryMiddleware(GlobalTrajectoryMiddleware):
    """Keep trajectory logging concise while preserving event prefixes."""

    def _format_prefix(self, meta: EventMeta) -> str:
        prefix = super()._format_prefix(meta)
        return prefix.rstrip(": ")

    def _format_payload(self, value: Any) -> str:
        return ""


class DemoStack:
    """Starts/stops all agents and provides stdin/stdout runtime flow."""

    def __init__(self) -> None:
        setup_env()
        self.host = os.getenv("AGENT_HOST", "localhost")
        self.examples_dir = Path(__file__).resolve().parent
        self.processes: list[subprocess.Popen[str]] = []

    def _port_for(self, port_env: str) -> int:
        value = os.getenv(port_env)
        if value:
            return int(value)

        fallback = DEFAULT_PORTS.get(port_env)
        if fallback is not None:
            return fallback

        raise RuntimeError(f"Missing required environment variable: {port_env}")

    def _is_port_open(self, host: str, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.25)
            return sock.connect_ex((host, port)) == 0

    def _wait_for_port(self, host: str, port: int, timeout_s: float = 45.0) -> None:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            if self._is_port_open(host, port):
                return
            time.sleep(0.25)
        raise TimeoutError(f"Timed out waiting for {host}:{port} to become ready")

    def start_all(self) -> None:
        print("Starting all A2A healthcare demo agents...", flush=True)
        launch_env = os.environ.copy()
        launch_env.setdefault("AGENT_HOST", self.host)
        for key, value in DEFAULT_PORTS.items():
            launch_env.setdefault(key, str(value))

        healthcare_agent = next(
            agent for agent in AGENTS if agent.port_env == "HEALTHCARE_AGENT_PORT"
        )
        dependency_agents = [
            agent for agent in AGENTS if agent.port_env != "HEALTHCARE_AGENT_PORT"
        ]

        for agent in dependency_agents:
            port = self._port_for(agent.port_env)
            proc = subprocess.Popen(
                ["uv", "run", agent.script],
                cwd=self.examples_dir,
                env=launch_env,
                stdout=None,
                stderr=None,
                text=True,
            )
            self.processes.append(proc)
            print(f"  • launched {agent.name} on port {port} (pid={proc.pid})", flush=True)

        for agent in dependency_agents:
            port = self._port_for(agent.port_env)
            self._wait_for_port(self.host, port)
            print(f"  ✓ {agent.name} is ready at http://{self.host}:{port}", flush=True)

        healthcare_port = self._port_for(healthcare_agent.port_env)
        healthcare_proc = subprocess.Popen(
            ["uv", "run", healthcare_agent.script],
            cwd=self.examples_dir,
            env=launch_env,
            stdout=None,
            stderr=None,
            text=True,
        )
        self.processes.append(healthcare_proc)
        print(
            f"  • launched {healthcare_agent.name} on port {healthcare_port} "
            f"(pid={healthcare_proc.pid})",
            flush=True,
        )

        self._wait_for_port(self.host, healthcare_port)
        print(
            f"  ✓ {healthcare_agent.name} is ready at http://{self.host}:{healthcare_port}",
            flush=True,
        )

    def stop_all(self) -> None:
        if not self.processes:
            return

        print("Shutting down all managed agents...", flush=True)
        for proc in self.processes:
            if proc.poll() is None:
                proc.terminate()

        deadline = time.time() + 8
        for proc in self.processes:
            while proc.poll() is None and time.time() < deadline:
                time.sleep(0.1)
            if proc.poll() is None:
                proc.kill()

        self.processes.clear()

    async def _build_healthcare_agent(self) -> A2AAgent:
        healthcare_port = self._port_for("HEALTHCARE_AGENT_PORT")
        healthcare_agent = A2AAgent(
            url=f"http://{self.host}:{healthcare_port}",
            memory=UnconstrainedMemory(),
        )
        await healthcare_agent.check_agent_exists()
        return healthcare_agent

    async def run_stdio_loop(self) -> None:
        healthcare_agent = await self._build_healthcare_agent()
        is_tty = sys.stdin.isatty()

        print("\nAll agents are running.", flush=True)
        if is_tty:
            print("Enter prompts (type 'exit' or 'quit' to stop).", flush=True)

        while True:
            try:
                if is_tty:
                    prompt = await asyncio.to_thread(input, "you> ")
                else:
                    prompt = await asyncio.to_thread(sys.stdin.readline)
                    if prompt == "":
                        return
                user_input = prompt.strip()
            except EOFError:
                return
            except KeyboardInterrupt:
                if is_tty:
                    print("", flush=True)
                    continue
                return

            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                return

            response = await healthcare_agent.run(user_input).middleware(
                ConciseGlobalTrajectoryMiddleware()
            )
            print(response.last_message.text, flush=True)


def main() -> None:
    stack = DemoStack()

    def _handle_signal(_: int, __: object) -> None:
        stack.stop_all()
        sys.exit(0)

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    try:
        stack.start_all()
        asyncio.run(stack.run_stdio_loop())
    finally:
        stack.stop_all()


if __name__ == "__main__":
    main()
