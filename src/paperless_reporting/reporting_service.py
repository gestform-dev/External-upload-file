import json
import time
from paperless_kafka.kafka_producer import KafkaProducerSingleton
from . import constants


class ReportingService:

    def __init__(self, asyncioLoop=False):
        self.asyncioLoop = asyncioLoop
        self._kafka_service = KafkaProducerSingleton(asyncioLoop)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def send_reporting(
        self,
        action: str,
        payload: any,
        project: str,
        dossierId: str = constants.MESSAGE_NC,
        correlationId: str = constants.MESSAGE_NC,
        operatorId: str = constants.UPLOADFILE_PROGRAM,
        topic: str = constants.KAFKA_TOPIC_WORKFLOW_STATE
    ):
        message = json.dumps({
            "stage": constants.RECEPTION,
            "payload": payload,
            "project": project,
            "action": action,
            "site": constants.MESSAGE_NC,
            "correlationId": correlationId,
            "dossierId": dossierId,
            "operatorId": operatorId,
            "timestamp": int(round(time.time() * 1000))
        }, default=str, ensure_ascii=False)

        if self.asyncioLoop:
            self._kafka_service.send_message_asyncio(topic, message)
        else:
            self._kafka_service.send_message(topic, message)
