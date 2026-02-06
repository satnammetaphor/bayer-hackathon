from datetime import datetime, timedelta, timezone
from typing import List

from incident_commander.agents.base import AgentResult


class DeployIntelligenceAgent:
    name = "DeployIntelligenceAgent"

    def analyze(self, events: List[dict]) -> AgentResult:
        deployments = [
            event
            for event in events
            if event.get("type") == "deploy"
        ]
        findings: List[str] = []
        signals = {"recent_deploy": "false"}
        if deployments:
            latest = max(deployments, key=lambda event: event.get("timestamp", ""))
            findings.append(
                f"Latest deployment {latest.get('deployment_id')} at {latest.get('timestamp')}."
            )
            signals["recent_deploy"] = "true"
        window_start = datetime.now(timezone.utc) - timedelta(minutes=30)
        recent = [
            event for event in deployments
            if _parse_iso(event.get("timestamp")) >= window_start
        ]
        if recent:
            findings.append(f"{len(recent)} deployments within the last 30 minutes.")
        return AgentResult(agent=self.name, findings=findings, signals=signals)


def _parse_iso(value: str | None) -> datetime:
    if not value:
        return datetime.fromtimestamp(0, tz=timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
