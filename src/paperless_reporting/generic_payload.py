from . import constants
from django.contrib.auth import get_user_model

User = get_user_model()


def create_generic_payload_from_user(user: User):
    return {
                constants.REGISTRATIONNUMBER_LABEL: user.matricule,
                constants.TECHNICAL_CLIENT_ID : user.technical_client_id,
                constants.COMPANY_LABEL: user.organization,
                constants.LASTNAME_LABEL: user.last_name,
                constants.FIRSTNAME_LABEL: user.first_name,
                constants.DATEOFBIRTH_LABEL: user.date_of_birth,
                constants.EMAIL_LABEL: user.email,
                constants.PHONENUMBER_LABEL: user.phone_number
            }