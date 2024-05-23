from django.apps import AppConfig


class PaperlessSendSmsConfig(AppConfig):
    name = "paperless_send_sms"

    def ready(self):
        AppConfig.ready(self)
