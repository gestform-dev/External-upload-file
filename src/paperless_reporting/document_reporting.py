import logging

from . import constants
from .reporting_service import ReportingService
from .generic_payload import create_generic_payload_from_user
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger("paperless_reporting")


def deposit_document_success_reporting(
    user: User,
    filename: str,
    correlationId: str,
    file_format: str,
    file_size_in_bytes: int,
    ):
    with ReportingService(asyncioLoop=False) as reporting_service:
        logger.info(
            "send trace reporting {}, user {} ".format(
                constants.ACTION_RECEPTION_DEPOSIT_DOCUMENT, user.username
                )
            )

        payload = create_generic_payload_from_user(user)
        payload[constants.FILENAME_LABEL] = filename
        payload[constants.FORMAT_LABEL] = file_format
        payload[constants.SIZE_IN_BYTES_LABEL] = file_size_in_bytes
        payload[constants.PATH_LABEL] = constants.MESSAGE_NC

        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_DEPOSIT_DOCUMENT,
            correlationId=correlationId,
            dossierId=filename,
            project=user.activity,
            payload=payload,
            operatorId=user.pk
            )


def deposit_document_failure_reporting(
    user: User,
    filename: str,
    correlationId: str,
    file_format: str,
    file_size_in_bytes: int,
    error: str = None,
    ):
    with ReportingService(asyncioLoop=False) as reporting_service:
        logger.info(
            f"send trace reporting "
            f"{constants.ACTION_RECEPTION_DEPOSIT_ERROR}, user "
            f"{user.username}, error {error}"
            )

        payload = create_generic_payload_from_user(user)
        payload[constants.FILENAME_LABEL] = filename
        payload[constants.FORMAT_LABEL] = file_format
        payload[constants.SIZE_IN_BYTES_LABEL] = file_size_in_bytes
        payload[constants.PATH_LABEL] = constants.MESSAGE_NC
        payload[constants.ERROR_LABEL] = error

        reporting_service.send_reporting(
            action=constants.ACTION_RECEPTION_DEPOSIT_ERROR,
            correlationId=correlationId,
            dossierId=constants.MESSAGE_NC,
            project=user.activity,
            payload=payload,
            operatorId=user.pk
            )
