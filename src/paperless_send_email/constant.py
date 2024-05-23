KAFKA_TOPIC_SEND_EMAIL = "send-email"

TEMPLATE_CONFIG_JSON = 'configs/default_template_config.json'

FROM_EMAIL = "no-reply@paperless.com"
SEND_EMAIL_TYPE = "SEND_EMAIL_TYPE"

USER_LABEL = "user"
FILE_LABEL = "file"
DATA_LABEL = "data"
LABEL_LABEL = "label"
EXTRACTED_KEY_LABEL = "extracted_key"
TYPE_LABEL = "type"
CONSTANT_LABEL = "constant"
VALUE_LABEL = "value"
LAST_NAME_LABEL = "last_name"
FIRST_NAME_LABEL = "first_name"
SUBJECT_LABEL = "subject"
INPUT_LABEL = "input"
PROJECT_LABEL = "project"
NC_LABEL = "NC"
USER_CONFIG_LABEL = "user_config"
NO_USER_DEFAULT_VALUE_LABEL = "no_user_default_value"

REGEX_EXTRACT_DATA_ON_SUBJECT = r"{{[^({{)(}})]*}}"
EXTRACT_DATA_ON_SUBJECT_BRACKETS_IN = "{{"
EXTRACT_DATA_ON_SUBJECT_BRACKETS_OUT = "}}"

LINE_BREAK = "\n"
SPACE_TAB = "\t"

LXML_PARSER = "lxml"

ERROR_EMAIL_TYPE_BAD_FORMAT = "email_type bad format"
ERROR_EMAIL_TEMPLATE_NOT_FOUND = "email template not found"
