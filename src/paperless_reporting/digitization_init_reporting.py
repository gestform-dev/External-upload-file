import logging
from datetime import datetime
import os
from .reporting_service import ReportingService
from . import constants
from .generic_payload import create_generic_payload_from_user
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger("paperless_management")


def deposit_document_digitization_init(
    user: User,
    originalFileName: str,
    filename: str,
    correlationId: str,
    file_format: str,
    file_size_in_bytes: int,
    receptionDate: datetime
    ):
    with ReportingService(asyncioLoop=False) as reporting_service:
        logger.info(
            "send trace reporting {}, user {} ".format(
                constants.ACTION_DIGITIZATION_INIT, user.username
                )
            )

        original_render_path = os.getenv(constants.ORIGINAL_RENDER_PATH)
        payload = create_generic_payload_from_user(user)

        payload[constants.FILENAME_LABEL] = filename
        payload[constants.FORMAT_LABEL] = file_format
        payload[constants.SIZE_IN_BYTES_LABEL] = file_size_in_bytes
        payload[constants.ORIGINALFILENAME_LABEL] = originalFileName
        payload[constants.PATH_LABEL] = original_render_path + filename
        payload[constants.ORIGINALFILEPATH_LABEL] = (original_render_path
                                                     + filename)
        payload[constants.RECEPTION_DATE] = receptionDate.isoformat()

        reporting_service.send_reporting(
            topic=constants.KAFKA_TOPIC_WORKFLOW_CMD,
            action=constants.ACTION_DIGITIZATION_INIT,
            correlationId=correlationId,
            dossierId=filename,
            project=user.activity,
            payload=payload,
            operatorId=user.pk
            )
