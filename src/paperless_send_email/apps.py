from django.apps import AppConfig


class PaperlessSendEmailConfig(AppConfig):
    name = "paperless_send_email"

    def ready(self):
        AppConfig.ready(self)
