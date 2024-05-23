import logging
import os

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm
    )
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from paperless.validators import FrenchPhoneNumberValidator
from paperless_management import constants
from paperless_management.config_management import ConfigManagement
from paperless_management.forgot_password_management import (
    forgot_password_success_management,
    )
from . import constants as paperless_constants

logger = logging.getLogger('paperless.auth')

User = get_user_model()


def _strings_to_html_for_password_help_text(password_rules):
    html_help_text = paperless_constants.PASSWORD_VALIDATION_FORMAT_START
    for rule in password_rules:
        formatted_rule = ("<li>"
                          + rule
                          + "</li>")
        html_help_text = html_help_text + formatted_rule
    html_help_text = (html_help_text +
                      paperless_constants.PASSWORD_VALIDATION_FORMAT_END)
    return html_help_text


class UserForgotPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].label = False
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
        ):
        logger.debug(context)
        resetUrl = (f"{os.getenv('PAPERLESS_URL')}/accounts/reset/"
                    f"{context['uid']}/{context['token']}/")
        logger.debug(resetUrl)
        forgot_password_success_management(context["user"], resetUrl)

    class Meta:
        model = User
        fields = ['email']


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        (self.fields['new_password1']
         .help_text) = _strings_to_html_for_password_help_text(
            paperless_constants
            .PASSWORD_VALIDATION_RULES)
        # this placeholder needs to be here for password visialization
        self.fields['new_password1'].widget.attrs['placeholder'] = ''
        self.fields['new_password2'].widget.attrs['placeholder'] = ''


class CustomUserCreationForm(UserCreationForm):
    username = forms.EmailField(label='Email')
    date_of_birth = forms.DateField(
        label=_('Date of birth (dd/mm/yyyy)'),
        # Placeholder does not exist on inpute date: common trick used.
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'type': "date"
                }),
        )
    phone_number = PhoneNumberField(
        label=_('Phone number (ex: 0612345678)'),
        validators=[FrenchPhoneNumberValidator()],
        region='FR',
        required=False,
        )
    phone_number.widget.attrs = {'type': 'tel',
                                 'inputmode': "numeric"}

    phone_number.error_messages['invalid'] = _('Incorrect format, use a valid'
                                               ' French mobile number')
    activity = forms.CharField(required=False, widget=forms.HiddenInput())
    matricule = forms.CharField(required=False, widget=forms.HiddenInput())
    confidentiality_checkbox = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        (self.fields['password1']
         .help_text) = _strings_to_html_for_password_help_text(
            paperless_constants.PASSWORD_VALIDATION_RULES)
        self.fields['password2'].help_text = (paperless_constants
                                              .SIGN_UP_REQUIRED_HELP_TEXT)
        (self.fields['confidentiality_checkbox']
         .help_text) = (paperless_constants.
                        CONFIDENTIALITY_POLICY_MESSAGE)

        self.fields['date_of_birth'].widget = forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'type': "date",
                })

    def create_invalid_user(self):
        return User(
            username=self[paperless_constants.USERNAME].value(),
            email=self[paperless_constants.USERNAME].value(),
            first_name=self[paperless_constants.FIRST_NAME].value(),
            last_name=self[paperless_constants.LAST_NAME].value(),
            date_of_birth=self[paperless_constants.DATE_OF_BIRTH].value(),
            matricule=paperless_constants.NA,
            organization=paperless_constants.NA,
            technical_client_id=paperless_constants.NA
            )

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self['username'].value()

        if commit:
            user.save()
        return user

    def try_define_additionals_fields(self, user,
                                      valid_users_in_first_activity):
        user.activity = valid_users_in_first_activity[
            constants.ACTIVITY_LABEL]
        config = ConfigManagement()
        try:
            db_matricule_column_name = config.get_db_column_name(
                user.activity,
                constants.MATRICULE_LABEL)
            db_organization_column_name = config.get_db_column_name(
                user.activity,
                constants.ORGANIZATION_LABEL)
            db_technical_client_id_column_name = config.get_db_column_name(
                user.activity,
                constants.TECHNICAL_CLIENT_ID)
            valid_user_in_first_db = \
                valid_users_in_first_activity[constants.USER_LABEL][0][
                    constants.USER_LABEL]

            _user_in_db_matricule = (
                valid_user_in_first_db[db_matricule_column_name])
            _user_in_db_organization = (
                valid_user_in_first_db[db_organization_column_name])
            _user_in_db_db_technical_client_id = (
                valid_user_in_first_db[db_technical_client_id_column_name])

            if _user_in_db_matricule is not None:
                user.matricule = _user_in_db_matricule
            if _user_in_db_organization is None:
                user.organization = user.activity
            else:
                user.organization = _user_in_db_organization
            if (_user_in_db_db_technical_client_id is None):
                user.technical_client_id = ''
            else:
                user.technical_client_id = _user_in_db_db_technical_client_id
        except KeyError:
            logger.debug(
                "Error occurred while trying to define specific fields")

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            _('date_of_birth'),
            'phone_number',
            'password1',
            'password2',
            ]
        exclude = [
            'activity',
            'matricule',
            'technical_client_id'
            ]
