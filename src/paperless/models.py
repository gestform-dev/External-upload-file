from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.conf import settings as guardian_settings
from phonenumber_field.modelfields import PhoneNumberField
from . import constants


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(
        verbose_name="date of birth", null=True, blank=True
        )
    activity = models.CharField(verbose_name="activity", max_length=150,
                                blank=True)
    matricule = models.CharField(verbose_name="matricule", max_length=50,
                                 blank=True, null=True)
    organization = models.CharField(verbose_name="organization", max_length=50,
                                    blank=True, null=True)
    technical_client_id = models.CharField(verbose_name="technical_client_id",
                                           max_length=50, blank=True,
                                           null=True)
    phone_number = PhoneNumberField(verbose_name="phone_number", max_length=15,
                                    blank=True, null=True)

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        super(CustomUser, self).save(*args, **kwargs)


def get_anonymous_user_instance(User):
    kwargs = {User.USERNAME_FIELD: guardian_settings.ANONYMOUS_USER_NAME}
    user = CustomUser(**kwargs)
    user.set_unusable_password()

    return user
