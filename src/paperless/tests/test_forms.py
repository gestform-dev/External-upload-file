import os

from django.test import TestCase
from paperless.forms import FrenchPhoneNumberValidator

class TestFrenchPhoneNumberValidator(TestCase):

    def setUp(self):
        self.frenchPhoneNumberValidator = FrenchPhoneNumberValidator()

    def test_is_valid_french_number_returns_true_for_0659507744(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('0659507744'),True)
    
    def test_is_valid_french_number_returns_true_for_0033659507744(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('0033659507744'),True)

    def test_is_valid_french_number_returns_true_for_plus_33659507744(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('+33659507744'),True)

    def test_is_valid_french_number_returns_true_for_0759507744(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('0759507744'),True)

    def test_is_valid_french_number_returns_false_for_9507744(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('9507744'),False)
    
    def test_is_valid_french_number_returns_false_for_plus_35659507744(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('+35659507744'),False)

    def test_is_valid_french_number_returns_false_for_0034659507744(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('0034659507744'),False)
    
    def test_is_valid_french_number_returns_false_for_0559507744(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('0559507744'),False)
    
    def test_is_valid_french_number_returns_false_when_number_is_too_long(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('05659507654654646543744'),False)
    
    def test_is_valid_french_number_returns_false_when_number_contains_letters(self):
        self.assertEqual(self.frenchPhoneNumberValidator.is_valid_french_number('0659507733aaaa'),False)

    
