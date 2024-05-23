from django.apps import AppConfig


class PaperlessReportingConfig(AppConfig):
    name = "paperless_reporting"

    def ready(self):
        AppConfig.ready(self)
