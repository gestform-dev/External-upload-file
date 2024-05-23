import logging
from . import constants
from .reporting_service import ReportingService
from django.contrib.auth import get_user_model
from .generic_payload import create_generic_payload_from_user

User = get_user_model()
logger = logging.getLogger("paperless_reporting")


def create_account_success_reporting(user: User):
    with ReportingService(asyncioLoop=True) as reporting_service:
        logger.info(
            f"send trace reporting"
            f" {constants.ACTION_RECEPTION_CREATE_ACCOUNT}, "
            f"user {user.username} ")
        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_CREATE_ACCOUNT,
            project=user.activity,
            payload=create_generic_payload_from_user(user),
            operatorId=user.pk
            )


def modify_account_success_reporting(user: User):
    with ReportingService(asyncioLoop=True) as reporting_service:
        logger.info(
            "send trace reporting"
            f"{constants.ACTION_RECEPTION_ACCOUNT_MODIFIED},"
            f" user {user.username} ")

        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_ACCOUNT_MODIFIED,
            project=user.activity,
            payload=create_generic_payload_from_user(user),
            operatorId=user.pk
            )


def modify_account_password_success_reporting(user: User, status: str = None):
    payload = create_generic_payload_from_user(user)
    payload[constants.STATUS_LABEL] = constants.UPDATE_PASSWORD_LABEL

    if status == constants.RESET_PASSWORD_LABEL:
        payload[constants.STATUS_LABEL] = constants.RESET_PASSWORD_LABEL

    with ReportingService(asyncioLoop=True) as reporting_service:
        logger.info(
            "send trace reporting"
            f" {constants.ACTION_RECEPTION_ACCOUNT_PASSWORD_MODIFIED},"
            f" user {user.username} ")
        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_ACCOUNT_PASSWORD_MODIFIED,
            project=user.activity,
            payload=payload,
            operatorId=user.pk
            )


def log_in_account_success_reporting(user: User):
    with ReportingService(asyncioLoop=True) as reporting_service:
        logger.info(
            "send trace reporting"
            f" {constants.ACTION_RECEPTION_ACCOUNT_LOGGED},"
            f" user {user.username} ")

        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_ACCOUNT_LOGGED,
            project=user.activity,
            payload=create_generic_payload_from_user(user),
            operatorId=user.pk
            )


def create_account_failure_reporting(user: any, errorLabel: str,
                                     error_description: str):
    with ReportingService(asyncioLoop=True) as reporting_service:
        logger.info(
            "send trace reporting "
            f"{constants.ACTION_RECEPTION_FAILURE_CREATE_ACCOUNT},"
            f" user {user.username} ")

        payload = create_generic_payload_from_user(user)
        payload["errorLabel"] = errorLabel
        payload["errorDescription"] = error_description

        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_FAILURE_CREATE_ACCOUNT,
            project=user.activity,
            payload=payload,
            operatorId=user.pk
            )


def modify_account_failure_reporting(user: any, errorLabel: any):
    with ReportingService(asyncioLoop=True) as reporting_service:
        logger.info(
            "send trace reporting "
            f"{constants.ACTION_RECEPTION_FAILURE_CREATE_ACCOUNT},"
            f" user {user.username} ")

        payload = create_generic_payload_from_user(user)
        payload["errorLabel"] = errorLabel
        payload["errorDescription"] = ""

        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_FAILURE_CREATE_ACCOUNT,
            project=user.activity,
            payload=payload,
            operatorId=user.pk
            )


def modify_account_password_failure_reporting(user: any,
                                              errorLabel: str,
                                              error_status: str):
    with ReportingService(asyncioLoop=True) as reporting_service:
        logger.info(
            "send trace reporting "
            f"{constants.ACTION_RECEPTION_FAILURE_CREATE_ACCOUNT},"
            f" user {user.username} ")

        payload = create_generic_payload_from_user(user)
        payload["errorLabel"] = errorLabel
        payload["errorDescription"] = ""
        payload["status"] = error_status

        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_FAILURE_CREATE_ACCOUNT,
            project=user.activity,
            payload=payload,
            operatorId=user.pk
            )
