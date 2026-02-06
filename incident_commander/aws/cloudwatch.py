import json
import time
from dataclasses import dataclass
from typing import Iterable, List, Optional

import boto3
from botocore.exceptions import ClientError


@dataclass
class CloudWatchConfig:
    log_group: str
    log_stream: str
    region: str


class CloudWatchLogsClient:
    def __init__(self, config: CloudWatchConfig) -> None:
        self._config = config
        self._client = boto3.client("logs", region_name=config.region)

    def ensure_group_and_stream(self) -> None:
        try:
            self._client.create_log_group(logGroupName=self._config.log_group)
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                raise
        try:
            self._client.create_log_stream(
                logGroupName=self._config.log_group,
                logStreamName=self._config.log_stream,
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                raise

    def put_events(self, messages: Iterable[dict]) -> None:
        self.ensure_group_and_stream()
        events = [
            {
                "timestamp": int(time.time() * 1000),
                "message": json.dumps(message),
            }
            for message in messages
        ]
        kwargs = {
            "logGroupName": self._config.log_group,
            "logStreamName": self._config.log_stream,
            "logEvents": events,
        }
        sequence_token = self._get_sequence_token()
        if sequence_token:
            kwargs["sequenceToken"] = sequence_token
        self._client.put_log_events(**kwargs)

    def read_events(self, limit: int = 200) -> List[dict]:
        response = self._client.get_log_events(
            logGroupName=self._config.log_group,
            logStreamName=self._config.log_stream,
            limit=limit,
            startFromHead=True,
        )
        events: List[dict] = []
        for event in response.get("events", []):
            try:
                events.append(json.loads(event["message"]))
            except json.JSONDecodeError:
                events.append({"raw": event["message"]})
        return events

    def _get_sequence_token(self) -> Optional[str]:
        response = self._client.describe_log_streams(
            logGroupName=self._config.log_group,
            logStreamNamePrefix=self._config.log_stream,
        )
        streams = response.get("logStreams", [])
        if not streams:
            return None
        return streams[0].get("uploadSequenceToken")
