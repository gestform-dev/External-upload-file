from django.apps import AppConfig


class PaperlessManagementConfig(AppConfig):
    name = "paperless_management"

    def ready(self):
        AppConfig.ready(self)
