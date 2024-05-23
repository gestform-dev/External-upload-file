import logging
from datetime import datetime

from paperless_reporting.account_reporting import (
    create_account_success_reporting,
    modify_account_success_reporting,
    modify_account_password_success_reporting,
    log_in_account_success_reporting,
    create_account_failure_reporting,
    modify_account_failure_reporting,
    modify_account_password_failure_reporting
)
from paperless_send_email.configs.email_config import EmailConfig
from paperless_send_email.configs.email_template_enum import EmailTemplateEnum
from paperless_send_email.mail_service import MailService
from paperless_send_sms.configs.sms_config import SmsConfig
from paperless_send_sms.configs.sms_template_enum import SmsTemplateEnum
from paperless_send_sms.sms_service import SmsService
from . import constants
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger("paperless_management")


def create_account_success_management(user: User,
                                      send_email: bool = True,
                                      send_sms: bool = False):
    # Send email
    if send_email:
        with (EmailConfig(user) as email_config,
              MailService(asyncioLoop=True) as mail_service):
            # add extra email config: filename, deposit_date,
            #  ... depending template
            email_config.deposit_date = (datetime.now()
                                         .strftime(constants.DATETIME_FORMAT))
            mail_service.send_email(email_config,
                                    EmailTemplateEnum.ACCOUNT_CREATION_SUCCESS)
    # Send sms
    if send_sms:
        with (SmsConfig(user) as sms_config,
              SmsService(asyncioLoop=True) as sms_service):
            sms_service.send_sms(sms_config,
                                 SmsTemplateEnum.ACCOUNT_CREATION_SUCCESS)
    # Send reporting
    create_account_success_reporting(user)


def modify_account_success_management(user: User):
    modify_account_success_reporting(user)


def modify_account_password_success_management(user: User, status: str = None,
                                               send_sms: bool = False):
    modify_account_password_success_reporting(user, status)
    if send_sms:
        with (SmsConfig(user) as sms_config,
              SmsService(asyncioLoop=True) as sms_service):
            sms_service.send_sms(sms_config,
                                 SmsTemplateEnum.RESET_PASSWORD_SUCCESS)


def log_in_account_success_management(user: User):
    log_in_account_success_reporting(user)


def create_account_failure_management(user: User, error: any,
                                      error_description='',
                                      send_email: bool = False):
    if send_email:
        with (EmailConfig(user) as email_config,
              MailService(asyncioLoop=True) as mail_service):
            mail_service.send_email(
                email_config, EmailTemplateEnum.ACCOUNT_CREATION_FAILURE
            )
    create_account_failure_reporting(user, error, error_description)


def modify_account_failure_management(user: User, error: any):
    modify_account_failure_reporting(user, error)


def modify_account_password_failure_management(user: User, error: any,
                                               error_status: str):
    modify_account_password_failure_reporting(user, error, error_status)


class InMultiplePersonDbException(Exception):
    pass


class MissingEmployeeInPersonDbException(Exception):
    pass


class CreationException(Exception):
    pass


class RequiredFieldException(Exception):
    pass


class AdditionalFieldsException(Exception):
    pass
