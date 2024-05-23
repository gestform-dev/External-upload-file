import json
import logging
import re
import os

from bs4 import BeautifulSoup
from paperless_kafka.kafka_producer import KafkaProducerSingleton
from .html_generator_service import HtmlGeneratorService

from . import constant
from .configs.email_config import EmailConfig
from .configs.email_template_config import EmailTemplateConfig
from .configs.email_template_enum import EmailTemplateEnum
from .file_utils import FileUtils
from paperless_management.config_management import ConfigManagement

logger = logging.getLogger("paperless_send_email")


class MailService:

    def __init__(self, asyncioLoop=False):
        self.asyncioLoop = asyncioLoop
        self.kafka_service = KafkaProducerSingleton(asyncioLoop)
        self.html_generator = HtmlGeneratorService()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def send_email(self, email_config: EmailConfig,
                   email_type: EmailTemplateEnum):
        logger.info(
            f"send_email to {email_config.user.username} with template "
            f"{email_type}")
        email_template = self._set_email_template(email_config, email_type)
        logger.debug(f"EMAIL TEMPLATE : {email_template}")

        if self.asyncioLoop:
            self.kafka_service.send_message_asyncio(
                constant.KAFKA_TOPIC_SEND_EMAIL, json.dumps(email_template))
        else:
            self.kafka_service.send_message(constant.KAFKA_TOPIC_SEND_EMAIL,
                                            json.dumps(email_template))

    def _set_email_template(self, email_config: EmailConfig,
                            email_type: EmailTemplateEnum):
        current_template = self._get_current_template(email_type)
        template_data = self._set_template_data(email_config, current_template)
        template_html = self.generate_html_email_content(template_data,
                                                         current_template)
        template_text = self.generate_text_email_from_html(template_html)
        template_subject = self._set_template_subject(template_data,
                                                      current_template)
        return {"to": [{"address": email_config.user.username}],
                "msg": {"from": {"address": constant.FROM_EMAIL},
                        "subject": template_subject, "html": template_html,
                        "text": template_text, },
                "type": os.getenv(constant.SEND_EMAIL_TYPE)}

    @staticmethod
    def _get_current_template(email_type: EmailTemplateEnum):
        config_json = FileUtils.read_json_file(constant.TEMPLATE_CONFIG_JSON)
        if not isinstance(email_type, EmailTemplateEnum):
            raise Exception(constant.ERROR_EMAIL_TYPE_BAD_FORMAT)
        if email_type.value not in config_json:
            raise Exception(constant.ERROR_EMAIL_TEMPLATE_NOT_FOUND)
        current_template = config_json[email_type.value]

        return current_template

    def generate_html_email_content(self, template_data: any,
                                    current_template: any):
        template_html = FileUtils.read_file(
            current_template.get(constant.FILE_LABEL))
        try:
            html = self.html_generator.generate_html(template_html,
                                                     template_data)
            return html
        except Exception as e:
            raise Exception(
                f"[generate_html_email_content] Error processing data: "
                f"{str(e)}")

    @staticmethod
    def generate_text_email_from_html(template_html: str) -> str:
        soup = BeautifulSoup(template_html, features=constant.LXML_PARSER)
        return soup.get_text()

    def _set_template_subject(self, template_data: any,
                              current_template: any) -> str:
        raw_subject = current_template.get(constant.SUBJECT_LABEL)
        extracted_data_list = re.findall(
            constant.REGEX_EXTRACT_DATA_ON_SUBJECT, raw_subject)

        return self._update_raw_subject_from_extracted_data(raw_subject,
                                                            template_data,
                                                            extracted_data_list)

    @staticmethod
    def _update_raw_subject_from_extracted_data(raw_subject: str,
                                                template_data: any,
                                                extracted_data_list: any) -> \
        str:
        for extracted_data in extracted_data_list:
            filtered_data = extracted_data.replace(
                constant.EXTRACT_DATA_ON_SUBJECT_BRACKETS_IN, "").replace(
                constant.EXTRACT_DATA_ON_SUBJECT_BRACKETS_OUT, "")
            if filtered_data in template_data:
                value = template_data.get(filtered_data)
                if value is None:
                    value = constant.NC_LABEL
                raw_subject = raw_subject.replace(extracted_data, value)

        return raw_subject

    def _set_template_data(self, email_config: EmailConfig,
                           current_template: any):
        template_data = {}
        for data in current_template.get(constant.DATA_LABEL):
            value = self._get_value_from_email_config(email_config, data)
            template_data.update({data.get(constant.LABEL_LABEL): value})

        return template_data

    def _get_value_from_email_config(self, email_config: EmailConfig,
                                     data: EmailTemplateConfig) -> str:
        value = None
        if data.get(constant.TYPE_LABEL) == constant.USER_LABEL:
            value = self._get_user_value(
                data.get(constant.EXTRACTED_KEY_LABEL), email_config.user)
        if data.get(constant.TYPE_LABEL) == constant.USER_CONFIG_LABEL:
            value = self._get_user_config_value(
                data.get(constant.EXTRACTED_KEY_LABEL), email_config.user,
                data)
        if data.get(constant.TYPE_LABEL) == constant.INPUT_LABEL:
            if hasattr(email_config, data.get(constant.EXTRACTED_KEY_LABEL)):
                value = email_config[data.get(constant.EXTRACTED_KEY_LABEL)]
        if data.get(constant.TYPE_LABEL) == constant.CONSTANT_LABEL:
            value = data.get(constant.VALUE_LABEL)

        return value

    @staticmethod
    def _get_user_value(extracted_key: str, user: any) -> str:
        if extracted_key == constant.LAST_NAME_LABEL:
            return user.last_name
        if extracted_key == constant.FIRST_NAME_LABEL:
            return user.first_name  # TODO : add project on user model  # if
            # extracted_key == constant.PROJECT_LABEL:  #     return  #  #
            # user.project

    @staticmethod
    def _get_user_config_value(extracted_key: str, user: any,
                               data: EmailTemplateConfig) -> str:
        if user.activity not in [None, '']:
            config = ConfigManagement()
            templateMailConfig = config.get_template_mail_config(
                user.activity)
            if extracted_key in templateMailConfig and templateMailConfig[
                extracted_key] not in [None, '']:
                return templateMailConfig[extracted_key]
        else:
            defaultValue = None
            if constant.NO_USER_DEFAULT_VALUE_LABEL in data:
                defaultValue = data.get(constant.NO_USER_DEFAULT_VALUE_LABEL)
            return defaultValue
