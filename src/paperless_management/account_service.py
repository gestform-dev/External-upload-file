import logging
import os
import requests
import copy
from . import constants
from .config_management import ConfigManagement
from .account_management import create_account_failure_management, \
    MissingEmployeeInPersonDbException, CreationException
from .error_enum import AccountErrorLabelEnum
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger("paperless_management")


def _user_has_field(user_in_db, required_field, user: User):
    if user_in_db.get(required_field) is (None or ''):
        create_account_failure_management(
            user=user,
            error=(AccountErrorLabelEnum
                   .REQUIRED_FIELD_MISSING_IN_PERSON_DB.value),
            error_description=required_field
            )
        return False
    return True


def _user_have_required_fields(db_config, user_in_db: dict, user: User):
    all_required_fields_are_available = True
    required_fields_list = db_config.get(constants.REQUIRED_FIELDS_LABEL)
    if required_fields_list is None:
        return all_required_fields_are_available
    for required_field in required_fields_list:
        if not _user_has_field(user_in_db, required_field, user):
            all_required_fields_are_available = False
    return all_required_fields_are_available


class AccountService:
    url = ""
    personsConfig = {}
    config = None

    def __init__(self, activity, user, *args, **kwargs):
        converter_env = os.environ.copy()
        self.config = ConfigManagement()
        self.personsConfig = self.config.get_persons(activity)

        self.url = (f"{converter_env[constants.ENV_BDD_TRACKING_API_URL]}"
                    f"{constants.PERSON_PATH}")

        self.user = copy.deepcopy(user)
        self.user.date_of_birth = self._reformat_date_of_birth(
            self.user.date_of_birth)

    def get_valid_users_in_config(self, user: User):
        persons_db_configs = self.personsConfig
        userInDbList = []
        for db_config in persons_db_configs:
            payload = self._build_query_payload(db_config)
            user_in_db = requests.get(self.url, params=payload)
            if user_in_db.status_code == 204:
                create_account_failure_management(
                    user,
                    (AccountErrorLabelEnum
                     .MISSING_EMPLOYEE_IN_PERSON_DB.value),
                    error_description=db_config[constants.ID_LABEL]
                    )
            elif user_in_db.status_code == 200:
                user_in_db_json = user_in_db.json()
                user_have_required_fields = (_user_have_required_fields(
                    db_config,
                    user_in_db_json,
                    user)
                )
                if user_have_required_fields:
                    userInDbList.append({'db': db_config[constants.DB_LABEL],
                                         'id': db_config[constants.ID_LABEL],
                                         'user': user_in_db_json})
            else:
                create_account_failure_management(
                    user,
                    AccountErrorLabelEnum.CREATION.value,
                    "status_code :" + str(user_in_db.status_code)
                    )
                raise CreationException
        return userInDbList

    def _build_query_payload(self, db_config):
        return f"""{constants.DB_LABEL}={db_config[constants.DB_LABEL]}""" \
               f"""{self._add_optional_table_filter(db_config)}""" \
               f"""{self._build_filters(db_config,
                                        db_config[
                                            (constants.
                                             VERIFICATION_FIELDS_LABEL)])}"""

    def _add_optional_table_filter(self, db_config):
        table_filter = ""
        try:
            table = db_config[constants.TABLE_LABEL]
        except KeyError:
            table = None
        if table:
            table_filter = f"&table={table}"
        return table_filter

    def _build_filters(self, db_config, fields):
        filters = ""
        for field in fields:
            filters = filters + f"&filters[type]={constants.NULL_LABEL}"
            filters = filters + (f"&lters[key]={db_config[constants.DB_FIELDS_ASSOCIATION_LABEL][field]}")
            filters = filters + f"&filters[value]={getattr(self.user, field)}"
        return filters

    def _reformat_date_of_birth(self, date):
        return date.strftime("%d.%m.%Y")


def get_valid_users(user: User):
    config = ConfigManagement()
    configList = config.get_configurations_list()
    userList = []
    for config in configList:
        valid_users_in_config = format_valid_users_in_config(config, user)
        if valid_users_in_config is not None:
            userList.append(valid_users_in_config)
    if len(userList) == 0:
        raise MissingEmployeeInPersonDbException
    if len(userList) > 1:
        create_account_failure_management(
            user,
            (AccountErrorLabelEnum
             .IN_MULTIPLE_PERSON_DB.value)
            )
    return userList


def format_valid_users_in_config(config, user):
    account = AccountService(
        config[constants.ACTIVITY_LABEL].value, user)
    valid_users_in_dbs = account.get_valid_users_in_config(user)
    if valid_users_in_dbs:
        return {
            constants.ACTIVITY_LABEL: config[
                constants.ACTIVITY_LABEL
            ].value,
            constants.ACTIVITY_LABEL: valid_users_in_dbs,
            }
    return None
