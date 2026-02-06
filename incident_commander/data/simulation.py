from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List


def build_simulated_events() -> List[dict]:
    now = datetime.now(timezone.utc)
    deploy_time = now - timedelta(minutes=15)
    return [
        {
            "type": "deploy",
            "deployment_id": "cfg-2026-05-12-001",
            "timestamp": deploy_time.isoformat(),
            "service": "checkout",
            "detail": "Connection pool size reduced from 40 to 10.",
        },
        {
            "type": "metric",
            "metric": "p99_latency_ms",
            "value": 2050,
            "timestamp": (now - timedelta(minutes=2)).isoformat(),
            "service": "checkout",
        },
        {
            "type": "log",
            "level": "ERROR",
            "service": "checkout",
            "timestamp": (now - timedelta(minutes=1)).isoformat(),
            "message": "DB connection timeout while handling request 9f1e2.",
        },
        {
            "type": "log",
            "level": "ERROR",
            "service": "checkout",
            "timestamp": now.isoformat(),
            "message": "DB connection timeout while handling request 9f1e3.",
        },
    ]
