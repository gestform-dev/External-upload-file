"""This module defines project-level constants."""

MIME_TYPE_HEIC = "image/heic"
MIME_TYPE_HEIF = "image/heif"
MIME_TYPE_JPEG = "image/jpeg"
HEIC_EXTENTION = ".heic"
JPG_EXTENTION = ".jpg"

MAX_PROGRESS_PERCENTAGE = 100

STARTING_STATUS = "STARTING"
SUCCESS_STATUS = "SUCCESS"
WORKING_STATUS = "WORKING"
FAILED_STATUS = "FAILED"

NUMERIC_FLOW_LABEL = "N"
PAPER_FLOW_LABEL = "P"
BATCH_LOT_LABEL = "LOT"
HYPHEN_LABEL = "-"

ADVANCE_UI_CONTENT_TYPE = "advanceui"
ADVANCE_UI_CONTENT_TYPE_VERBOSE = "advance ui"
ACCOUNT_SETTINGS_CONTENT_TYPE = "accountsettings"
ACCOUNT_SETTINGS_CONTENT_TYPE_VERBOSE = "account settings"
DOCUMENTS_LABEL = "documents"
NA_LABEL = "NA"

CORRELATION_ID_FORMAT = (
    lambda group, batch,
           flow_type,
           doc_index:
    f"{group}{HYPHEN_LABEL}{batch}{HYPHEN_LABEL}{flow_type}{doc_index}"
)
DEFAULT_ACTIVITY_NAME = "DEFAULT"
PREFIX_CONFIG_PATH = ("paperless_management/"
                      "user_configs/")
