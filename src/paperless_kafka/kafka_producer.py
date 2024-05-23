import logging
import os
from confluent_kafka import Producer, KafkaException
import asyncio
from threading import Thread
from . import constants

from .models import KafkaProducerStatus

logger = logging.getLogger("paperless_kafka")


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class KafkaProducerSingleton(Borg):
    def __init__(self, asyncioLoop=False):
        Borg.__init__(self)
        self.asyncioLoop = asyncioLoop
        if not hasattr(self, '_producer'):
            self._initialize_producer()
        if not hasattr(self, '_poll_thread') and asyncioLoop:
            self._loop = self.get_or_create_eventloop()
            self._cancelled = False
            self._poll_thread = Thread(target=self._poll_loop)
            self._poll_thread.start()

    def _initialize_producer(self, *args, **kwargs):
        kafka_broker = os.getenv(constants.KAFKA_BROKER)
        logger.info(f"[KafkaProducerSingleton], _initialize_producer: {kafka_broker}")
        self._producer = Producer({'bootstrap.servers': kafka_broker})

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(constants.TIMEOUT_POLL_ASYNCIO)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def send_message_asyncio(self, topic, message):
        """
        An awaitable produce method.
        """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                logger.error(f'[KafkaProducerSingleton, asyncio] Error on sending, err: {err}, kafka msg: {msg}, message: {message}')
                self._loop.call_soon_threadsafe(result.set_exception, KafkaException(err))
            else:
                logger.debug(f"[KafkaProducerSingleton, asyncio] Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}, message : {message}")
                self._loop.call_soon_threadsafe(result.set_result, msg)

        self._producer.produce(topic, value=message.encode(constants.ENCODE_UTF8), on_delivery=ack)
        return result

    def send_message(self, topic, message):
        # call with asyncioLoop=False; case document deposit, treatment on worker
        def ack(err, msg):
            if err:
                logger.error(f'[KafkaProducerSingleton, no asyncio] Error on sending, err: {err}, kafka msg: {msg}, message: {message}')
            else:
                logger.debug(f"[KafkaProducerSingleton, no asyncio] Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}, message : {message}")

        self._producer.produce(topic, value=message.encode(constants.ENCODE_UTF8), on_delivery=ack)
        self._producer.poll()

    @staticmethod
    def get_or_create_eventloop():
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if constants.ERROR_NO_CURRENT_EVENT_LOOP in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()
