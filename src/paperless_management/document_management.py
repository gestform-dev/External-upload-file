import logging
import mimetypes
from datetime import datetime
from . import constants

from paperless_reporting.document_reporting import (
    deposit_document_success_reporting,
    deposit_document_failure_reporting,
)
from paperless_reporting.digitization_init_reporting import (
    deposit_document_digitization_init,
)
from paperless_send_email.configs.email_config import EmailConfig
from paperless_send_email.configs.email_template_enum import EmailTemplateEnum
from paperless_send_email.mail_service import MailService
from documents.models import Document
from django.contrib.auth import get_user_model
from paperless_send_sms.configs.sms_config import SmsConfig
from paperless_send_sms.sms_service import SmsService
from paperless_send_sms.configs.sms_template_enum import SmsTemplateEnum

User = get_user_model()
logger = logging.getLogger("paperless_management")


def get_extension_from_mime_type(mime_type):
    extension = mimetypes.guess_extension(mime_type)
    return extension[1:]


def deposit_document_success_management(user: User,
                                        document: Document,
                                        file_size_in_bytes: int,
                                        send_email: bool = True,
                                        send_sms: bool = False):
    if send_email:
        with EmailConfig(user) as email_config, MailService(asyncioLoop=False) as mail_service:
            email_config.deposit_date = datetime.now().strftime(constants.DATETIME_FORMAT)
            mail_service.send_email(email_config,
                                    EmailTemplateEnum.DEPOSIT_DOCUMENT_SUCCESS)
    document_format = get_extension_from_mime_type(document.mime_type)
    deposit_document_success_reporting(
        user,
        document.original_filename,
        document.correlation_id,
        document_format,
        file_size_in_bytes,
    )
    deposit_document_digitization_init(
        user,
        document.original_filename,
        document.filename,
        document.correlation_id,
        document_format,
        file_size_in_bytes,
        receptionDate=document.created
    )
    if send_sms:
        with (SmsConfig(user) as sms_config,
              SmsService(asyncioLoop=False) as sms_service):
            sms_service.send_sms(sms_config,
                                 SmsTemplateEnum.DEPOSIT_DOCUMENT_SUCCESS)


def deposit_document_fail_management(
    user: User,
    file_name: str,
    correlation_id: str,
    mime_type: str,
    file_size_in_bytes: int,
    error: any = None,
    error_message: any = None,
    sendEmail: bool = True,
):
    if sendEmail:
        with EmailConfig(user, file_name, error_message) as email_config, MailService(asyncioLoop=False) as mail_service:
            email_config.deposit_date = datetime.now().strftime(constants.DATETIME_FORMAT)
            mail_service.send_email(email_config, EmailTemplateEnum.DEPOSIT_DOCUMENT_ERROR)
    document_format = get_extension_from_mime_type(mime_type)
    deposit_document_failure_reporting(
        user,
        file_name,
        correlation_id,
        document_format,
        file_size_in_bytes,
        error=error,
    )
