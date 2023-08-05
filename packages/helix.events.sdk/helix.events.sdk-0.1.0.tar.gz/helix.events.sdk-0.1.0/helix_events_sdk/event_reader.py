import os
from logging import Logger
from typing import Optional, Any

from cloudevents.http import CloudEvent, from_json
from kafka import KafkaConsumer


class BaseEventReader:
    def __init__(self, logger: Logger):
        self._logger = logger

    def read_next_event(self) -> CloudEvent:
        pass


class KafkaEventReader(BaseEventReader):
    def __enter__(self) -> BaseEventReader:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._consumer.close()

    def __init__(
        self,
        logger: Logger,
        topic: str,
        group_id: str,
        kafka_brokers: [str],
        use_ssl: bool = False
    ):
        security_protocol = "PLAINTEXT"
        if use_ssl:
            security_protocol = "SSL"

        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=kafka_brokers,
            group_id=group_id,
            consumer_timeout_ms=30000,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            security_protocol=security_protocol
        )
        super().__init__(logger)

    def read_next_event(self) -> CloudEvent:
        self._logger.info('waiting for messages')
        returned_event = next(self._consumer).value
        return from_json(returned_event)
