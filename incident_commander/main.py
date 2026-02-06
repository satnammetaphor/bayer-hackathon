import argparse
import json
from pathlib import Path

from incident_commander.aws.cloudwatch import CloudWatchConfig, CloudWatchLogsClient
from incident_commander.commander import CommanderAgent
from incident_commander.data.simulation import build_simulated_events


def _load_local_events(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Missing local events file: {path}")
    return json.loads(path.read_text())


def _save_local_events(path: Path, events: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(events, indent=2))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Autonomous Incident Commander")
    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate = subparsers.add_parser("simulate-logs", help="Send simulated events to CloudWatch Logs.")
    simulate.add_argument("--log-group", required=True)
    simulate.add_argument("--log-stream", required=True)
    simulate.add_argument("--region", default="us-east-1")

    local = subparsers.add_parser("simulate-local", help="Write simulated events to a local JSON file.")
    local.add_argument("--output", default="incident_commander/data/local_events.json")

    investigate = subparsers.add_parser("run-commander", help="Run the commander against events.")
    investigate.add_argument("--log-group")
    investigate.add_argument("--log-stream")
    investigate.add_argument("--region", default="us-east-1")
    investigate.add_argument("--local-events", default="incident_commander/data/local_events.json")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.command == "simulate-logs":
        events = build_simulated_events()
        client = CloudWatchLogsClient(
            CloudWatchConfig(
                log_group=args.log_group,
                log_stream=args.log_stream,
                region=args.region,
            )
        )
        client.put_events(events)
        print(f"Sent {len(events)} events to CloudWatch Logs.")
    elif args.command == "simulate-local":
        events = build_simulated_events()
        output = Path(args.output)
        _save_local_events(output, events)
        print(f"Wrote {len(events)} events to {output}.")
    elif args.command == "run-commander":
        if args.log_group and args.log_stream:
            client = CloudWatchLogsClient(
                CloudWatchConfig(
                    log_group=args.log_group,
                    log_stream=args.log_stream,
                    region=args.region,
                )
            )
            events = client.read_events()
        else:
            events = _load_local_events(Path(args.local_events))
        commander = CommanderAgent()
        report = commander.investigate(events)
        print("Incident Report")
        print("===============")
        print(report.summary)
        print("\nFindings:")
        for item in report.findings:
            print(f"- {item}")
        print("\nRecommendation:")
        print(report.recommendation)


if __name__ == "__main__":
    main()
