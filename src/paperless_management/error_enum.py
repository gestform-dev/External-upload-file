from enum import Enum


class AccountErrorLabelEnum(Enum):
    CREATION = "CREATION"
    IN_MULTIPLE_PERSON_DB = "IN_MULTIPLE_PERSON_DB"
    MISSING_EMPLOYEE_IN_PERSON_DB = "MISSING_EMPLOYEE_IN_PERSON_DB"
    REQUIRED_FIELD_MISSING_IN_PERSON_DB = "REQUIRED_FIELD_MISSING_IN_PERSON_DB"
    MODIFICATION = "MODIFICATION"
    PASSWORD_MODIFICATION = "PASSWORD_MODIFICATION"


class DocumentErrorLabelEnum(Enum):
    MESSAGE_DOCUMENT_ALREADY_EXISTS = "document_already_exists"
    MESSAGE_ASN_ALREADY_EXISTS = "asn_already_exists"
    MESSAGE_ASN_RANGE = "asn_value_out_of_range"
    MESSAGE_FILE_NOT_FOUND = "file_not_found"
    MESSAGE_FILE_EXTENSION_NOT_ALLOWED = "file_extension_not_allowed"
    MESSAGE_PRE_CONSUME_SCRIPT_NOT_FOUND = "pre_consume_script_not_found"
    MESSAGE_PRE_CONSUME_SCRIPT_ERROR = "pre_consume_script_error"
    MESSAGE_POST_CONSUME_SCRIPT_NOT_FOUND = "post_consume_script_not_found"
    MESSAGE_POST_CONSUME_SCRIPT_ERROR = "post_consume_script_error"
    MESSAGE_UNSUPPORTED_TYPE = "unsupported_type"
    MESSAGE_FILE_SIZE_TOO_LARGE = "file_size_too_large"
