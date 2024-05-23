import re
from phonenumber_field.phonenumber import to_python
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import logging
from .constants import (
    PASSWORD_SPECIAL_CHARACTERS,
    PASSWORD_VALIDATION_ERROR_LOWERCASES,
    PASSWORD_VALIDATION_ERROR_CAPITALS,
    PASSWORD_VALIDATION_ERROR_SYMBOLS,
    PASSWORD_VALIDATION_ERROR_NUMBERS,
    PASSWORD_VALIDATION_ERROR_LENGTH)
logger = logging.getLogger("paperless")


class FrenchPhoneNumberValidator:
    def __call__(self, value):
        # Remove any non-digit characters
        cleaned_value = re.sub(r'\D', '', str(value))

        # Check if the phone number is a valid French phone number
        if not self.is_valid_french_number(cleaned_value):
            raise ValidationError(
                _('Incorrect format, use a valid French mobile number'))

    def isFrenchMobile(self, phone_number):
        return (phone_number.as_e164.startswith('+336')
                or phone_number.as_e164.startswith('+337'))

    def is_valid_french_number(self, value):
        try:
            phone_number = to_python(value, 'FR')
            return (phone_number.is_valid()
                    and self.isFrenchMobile(phone_number))
        except Exception as e:
            logger.debug(e)
            return False


class CustomPasswordValidator:
    def __init__(self):
        self.number_of_lowercases = 1
        self.number_of_capitals = 1
        self.number_of_symbols = 1
        self.number_of_numbers = 1
        self.minimum_length = 12
        self.symbols = PASSWORD_SPECIAL_CHARACTERS

    def validate(self, password, user=None):
        lowercases = [char for char in password if char.islower()]
        capitals = [char for char in password if char.isupper()]
        symbols = [char for char in password if char in self.symbols]
        numbers = [char for char in password if char.isnumeric()]
        error_list = []
        if len(lowercases) < self.number_of_lowercases:
            capital_error = (
                PASSWORD_VALIDATION_ERROR_LOWERCASES)
            error_list.append(capital_error)
        if len(capitals) < self.number_of_capitals:
            capital_error = (PASSWORD_VALIDATION_ERROR_CAPITALS)
            error_list.append(capital_error)
        if len(symbols) < self.number_of_symbols:
            symbol_error = (PASSWORD_VALIDATION_ERROR_SYMBOLS)
            error_list.append(symbol_error)
        if len(password) < self.minimum_length:
            min_length_error = (PASSWORD_VALIDATION_ERROR_LENGTH)
            error_list.append(min_length_error)
        if len(numbers) < self.number_of_numbers:
            number_error = (PASSWORD_VALIDATION_ERROR_NUMBERS)
            error_list.append(number_error)
        if len(error_list) > 0:
            raise ValidationError(error_list)
