import os
from logging import Logger
from typing import Optional, Any

from cloudevents.http import CloudEvent, to_json
from kafka import KafkaProducer

from helix_events_sdk.events.audit import AuditEvent


class BaseEventWriter:
    def __init__(self, logger: Logger):
        self._logger = logger

    def write_event(self, event: CloudEvent) -> None:
        pass


class EventWriter(BaseEventWriter):
    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    def write_event(self, event: CloudEvent) -> None:
        self._logger.info("sending event")
        self._logger.info(event)


class KafkaEventWriter(BaseEventWriter):
    def __enter__(self) -> BaseEventWriter:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._producer.close()

    def __init__(
        self,
        logger: Logger,
        kafka_brokers: [str],
        use_ssl: bool = False
    ):
        security_protocol = "PLAINTEXT"
        if use_ssl:
            security_protocol = "SSL"

        self._producer = KafkaProducer(
            bootstrap_servers=kafka_brokers,
            security_protocol=security_protocol
        )
        super().__init__(logger=logger)

    def write_event(self, event: CloudEvent) -> None:
        topic = self._get_topic(event)
        self._producer.send(topic, to_json(event))

    def _get_topic(self, event: CloudEvent) -> str:
        if isinstance(event, AuditEvent):
            return 'audit'
        raise
