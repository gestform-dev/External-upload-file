import json
import logging

from paperless_kafka.kafka_producer import KafkaProducerSingleton

from . import constant
from .configs.sms_config import SmsConfig
from .configs.sms_template_enum import SmsTemplateEnum
from .file_utils import FileUtils

logger = logging.getLogger("paperless_send_sms")


class SmsService:

    def __init__(self, asyncioLoop=False):
        self.asyncioLoop = asyncioLoop
        self.kafka_service = KafkaProducerSingleton(asyncioLoop)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def send_sms(self, sms_config: SmsConfig, sms_type: SmsTemplateEnum):
        logger.info(f"send_sms to {sms_config.user.username}"
                    f" with template {sms_type}")
        if sms_config.user.phone_number not in [None, '']:
            sms_template = self._set_sms_template(sms_config, sms_type)
            logger.debug(f"SMS TEMPLATE : {sms_template}")

            if self.asyncioLoop:
                self.kafka_service.send_message_asyncio(
                    constant.KAFKA_TOPIC_SEND_SMS, json.dumps(sms_template))
            else:
                self.kafka_service.send_message(constant.KAFKA_TOPIC_SEND_SMS,
                                                json.dumps(sms_template))

    def _set_sms_template(self, sms_config: SmsConfig,
                          sms_type: SmsTemplateEnum):
        current_template = self._get_current_template(sms_type)

        campaign_name = current_template.get(constant.CAMPAIGN_NAME_LABEL)
        message = current_template.get(constant.MESSAGE_LABEL)
        return {
            "number": sms_config.user.phone_number.as_e164,
            "message": message,
            "sender": constant.SENDER_SMS,
            "campaignName": campaign_name
        }

    @staticmethod
    def _get_current_template(sms_type: SmsTemplateEnum):
        config_json = FileUtils.read_json_file(constant.TEMPLATE_CONFIG_JSON)
        if not isinstance(sms_type, SmsTemplateEnum):
            raise Exception(constant.ERROR_SMS_TYPE_BAD_FORMAT)
        if sms_type.value not in config_json:
            raise Exception(constant.ERROR_SMS_TEMPLATE_NOT_FOUND)
        current_template = config_json[sms_type.value]

        return current_template
