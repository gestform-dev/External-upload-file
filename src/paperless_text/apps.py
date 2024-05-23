from django.apps import AppConfig
from django.conf import settings


class PaperlessTextConfig(AppConfig):
    name = "paperless_text"

    def ready(self):
        if settings.TEXT_FORMAT_ENABLED_IN_CONSUMER:
            from paperless_text.signals import text_consumer_declaration
            from documents.signals import document_consumer_declaration
            document_consumer_declaration.connect(text_consumer_declaration)

        AppConfig.ready(self)
