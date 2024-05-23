from django.apps import AppConfig


class PaperlessKafkaConfig(AppConfig):
    name = "paperless_kafka"

    def ready(self):
        AppConfig.ready(self)
