from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

"""This module defines project-level constants."""

NEW_PASSWORD = 'newPassword'
CONFIRM_PASSWORD = 'confirmPassword'
PASSWORD = 'password'
INVALID_PASWWORD_ERROR_MESSAGE = _('Invalid password')
USERNAME = 'username'
EMAIL = 'email'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
DATE_OF_BIRTH = 'date_of_birth'
NA = 'NA'
FIELDS_IN_ERROR = 'fieldsInError'
REGISTRATION_SUCCESS_MESSAGE = "Registration successful."
REGISTRATION_FAILURE_MESSAGE = ("Unsuccessful registration."
                                "Invalid information.")
LOGIN_LABEL = "login"
BASE_LABEL = "base"

EMPLOYEE = 'employee'
ADD_DOCUMENT_PERMISSION = 'add_document'
CHANGE_DOCUMENT_PERMISSION = 'change_document'
VIEW_DOCUMENT_PERMISSION = 'view_document'
EMPLOYEE_GROUP_CREATED = 'Employee group created with necessary permissions'
ACTIVITY = 'activity'
RESET_PASSWORD_ERROR_STATUS = "resetPassword"
UPDATE_PASSWORD_ERROR_STATUS = "updatePassword"

RESET_PASSWORD_LABEL = 'resetPassword'
FR = 'FR'
PHONE_NUMBER = 'phone_number'
PHONE_NUMBER_ERROR_MESSAGE = ('Incorrect format,'
                              ' use a valid French mobile number')
PASSWORD_VALIDATION_ERROR_LOWERCASES = (
    _("Your password must contain at least 1 lowercase "))
PASSWORD_VALIDATION_ERROR_CAPITALS = (
    _("Your password must contain at least 1 capital "))
PASSWORD_VALIDATION_ERROR_SYMBOLS = (
    _("Your password must contain at least 1 symbol "))
PASSWORD_VALIDATION_ERROR_LENGTH = (
    _("Your password must be at least 12 characters "))
PASSWORD_VALIDATION_ERROR_NUMBERS = (
    _("Your password must contain at least 1 number "))
PASSWORD_VALIDATION_RULES = (
    _("At least 12 characters"),
    _("At least one uppercase letter and one lowercase letter"),
    _("At least a number"),
    _("At least one special character"))
SIGN_UP_REQUIRED_HELP_TEXT = _('* required fields')
PASSWORD_VALIDATION_FORMAT_START = (
    "<figure style='text-align:left;'>"
    "<figcaption>"
    + _("Your password must contain :")
    + "</figcaption>"
      "<ul style='text-align:left;'>")
PASSWORD_VALIDATION_FORMAT_END = ("</ul>"
                                  "</figure>")
PASSWORD_SPECIAL_CHARACTERS = "`~!@#$%^&*()|<,>_-=+{}\":;'[]/.?"
CONFIDENTIALITY_POLICY_STRING_END = _("privacy policy")
CONFIDENTIALITY_POLICY_MESSAGE = _("I accept the confidentiality policy"
                                   " transmitted by my company")
RESET_PASSWORD_EMAIL_TOASTER_SEARCH_PARAM = "?toaster=send-email"
RESET_PASSWORD_SUCCESS_TOASTER_SEARCH_PARAM = '?toaster=reset-password'
SIGN_UP_FAILED_TOASTER_SEARCH_PARAM = "?toaster=sign_up_failed"
