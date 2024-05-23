from django.db import models


class KafkaProducerStatus(models.Model):
    is_initialized = models.BooleanField(default=False)

