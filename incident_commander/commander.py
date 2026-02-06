from __future__ import annotations

from dataclasses import dataclass
from typing import List

from incident_commander.agents.base import AgentResult
from incident_commander.agents.deploy_intelligence_agent import DeployIntelligenceAgent
from incident_commander.agents.logs_agent import LogsAgent
from incident_commander.agents.metrics_agent import MetricsAgent


@dataclass
class IncidentReport:
    summary: str
    findings: List[str]
    recommendation: str


class CommanderAgent:
    def __init__(self) -> None:
        self._agents = [
            LogsAgent(),
            MetricsAgent(),
            DeployIntelligenceAgent(),
        ]

    def investigate(self, events: List[dict]) -> IncidentReport:
        results = [agent.analyze(events) for agent in self._agents]
        findings = self._summarize_findings(results)
        recommendation = self._recommendation(results)
        summary = "Latent configuration bug suspected after correlating logs, metrics, and deploys."
        return IncidentReport(summary=summary, findings=findings, recommendation=recommendation)

    def _summarize_findings(self, results: List[AgentResult]) -> List[str]:
        findings: List[str] = []
        for result in results:
            findings.extend([f"[{result.agent}] {item}" for item in result.findings])
        return findings

    def _recommendation(self, results: List[AgentResult]) -> str:
        signals = {key: value for result in results for key, value in result.signals.items()}
        if signals.get("latency_spike") == "true" and signals.get("recent_deploy") == "true":
            return "Rollback the most recent configuration deployment and monitor latency."
        if signals.get("latency_spike") == "true":
            return "Escalate to DB and platform teams; investigate connection pool limits."
        return "No immediate action required."
