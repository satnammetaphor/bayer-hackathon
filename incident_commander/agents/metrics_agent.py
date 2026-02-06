from typing import List

from incident_commander.agents.base import AgentResult


class MetricsAgent:
    name = "MetricsAgent"

    def analyze(self, events: List[dict]) -> AgentResult:
        spikes = [
            event
            for event in events
            if event.get("type") == "metric" and event.get("metric") == "p99_latency_ms"
            and event.get("value", 0) >= 2000
        ]
        findings = [
            f"{len(spikes)} latency spikes at or above 2000ms detected."
        ]
        signals = {"latency_spike": "true" if spikes else "false"}
        return AgentResult(agent=self.name, findings=findings, signals=signals)
