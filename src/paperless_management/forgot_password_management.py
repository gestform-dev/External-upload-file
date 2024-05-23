import logging

from paperless_send_email.configs.email_config import EmailConfig
from paperless_send_email.configs.email_template_enum import EmailTemplateEnum
from paperless_send_email.mail_service import MailService

logger = logging.getLogger("paperless_management")


def forgot_password_success_management(user: any, link, sendEmail: bool = True):
    if sendEmail:
        with EmailConfig(user) as email_config, MailService(asyncioLoop=True) as mail_service:
            email_config.link = link
            mail_service.send_email(email_config, EmailTemplateEnum.RESET_PASSWORD)
