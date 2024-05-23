import json
import logging

from . import constants
from .user_configs.user_configs_enum import UserConfigsEnum

logger = logging.getLogger("paperless_management")


class ConfigManagement:
    def get_configuration(self, activity):
        try:
            with open(f"{constants.CONFIG_BASE_PATH}"
                      f"{activity}{constants.JSON_FORMAT}") as payload:
                return json.load(payload)
        except Exception:
            return {}

    def get_configurations_list(self, key=None):
        list = []
        for activity in UserConfigsEnum:
            matching_config = None
            global_config = self.get_configuration(activity.value)
            if key:
                matching_config = global_config[key]
            config = {"activity": activity,
                      "config": matching_config or global_config, }
            list.append(config)
        return list

    def get_document_config(self, activity):
        config = self.get_configuration(activity)
        return config[constants.DOCUMENT_LABEL]

    def get_allowed_extensions(self, activity):
        config = self.get_configuration(activity)
        return (
            config[constants.DOCUMENT_LABEL][
                constants.ALLOWED_EXTENSIONS_LABEL])

    def get_batch_keyword(self, activity):
        config = self.get_configuration(activity)
        return config[constants.DOCUMENT_LABEL][constants.BATCH_KEYWORD_LABEL]

    def get_flow_type(self, activity):
        config = self.get_configuration(activity)
        return config[constants.DOCUMENT_LABEL][constants.FLOW_TYPE_LABEL]

    def get_max_allowed_size_in_MB(self, activity):
        config = self.get_configuration(activity)
        return (
            config[constants.DOCUMENT_LABEL][constants.MAX_ALLOWED_SIZE_IN_MB])

    def get_person(self, activity):
        config = self.get_configuration(activity)
        return config[constants.PERSONS_LABEL]

    def get_db_column_name(self, activity: str, field):
        config = self.get_configuration(activity)
        return (config[constants.PERSONS_LABEL][0][
            constants.DB_FIELDS_ASSOCIATION_LABEL][field])

    def get_template_mail_config(self, activity):
        config = self.get_configuration(activity)
        return config[constants.TEMPLATE_MAIL_CONFIG]

    def is_sms_enabled_for_action(self, activity, action):
        config = self.get_configuration(activity)
        return (action.value in (
            config[constants.NOTIFICATIONS_LABEL][
                constants.SMS_SETTINGS_LABEL]))
