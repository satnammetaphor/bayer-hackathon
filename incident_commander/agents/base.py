from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AgentResult:
    agent: str
    findings: List[str]
    signals: Dict[str, str]

