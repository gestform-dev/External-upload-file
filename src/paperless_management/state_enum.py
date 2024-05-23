from enum import Enum

# List of the application relevant states where we'd like to manage
# e.g: reporting, sending email or sms


class StateEnum(Enum):
    ACCOUNT_CREATION_SUCCESS = "ACCOUNT_CREATION_SUCCESS"
    DEPOSIT_FILE_SUCCESS = "DEPOSIT_FILE_SUCCESS"
    RESET_PASSWORD_SUCCESS = "RESET_PASSWORD_SUCCESS"
