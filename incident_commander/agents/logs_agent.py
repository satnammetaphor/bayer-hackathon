from typing import List

from incident_commander.agents.base import AgentResult


class LogsAgent:
    name = "LogsAgent"

    def analyze(self, events: List[dict]) -> AgentResult:
        errors = [
            event
            for event in events
            if event.get("type") == "log" and "timeout" in event.get("message", "").lower()
        ]
        findings = [
            f"{len(errors)} DB connection timeout errors detected in application logs."
        ]
        signals = {"log_error_type": "db_connection_timeout" if errors else "none"}
        return AgentResult(agent=self.name, findings=findings, signals=signals)
