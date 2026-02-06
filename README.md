# bayer-hackathon
Autonomous Incident Commander

## Overview
This prototype simulates CloudWatch logs/metrics and runs a commander agent that
coordinates log, metric, and deploy-intelligence agents to produce an incident
report. It can publish simulated events to AWS CloudWatch Logs or use local
JSON fixtures for offline demos.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Simulate events locally
```bash
python -m incident_commander.main simulate-local --output incident_commander/data/local_events.json
python -m incident_commander.main run-commander --local-events incident_commander/data/local_events.json
```

## Send simulated events to AWS CloudWatch Logs
Set AWS credentials via environment variables or your preferred AWS auth flow.
```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
python -m incident_commander.main simulate-logs --log-group bayer-hackathon --log-stream demo
```

## Run the commander against CloudWatch Logs
```bash
python -m incident_commander.main run-commander --log-group bayer-hackathon --log-stream demo
```
