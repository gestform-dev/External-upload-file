# from django.dispatch import receiver
# from django.db.models.signals import post_migrate
# from .tasks import initialize_kafka_producer_task
#
# @receiver(post_migrate)
# def initialize_kafka_producer(sender, **kwargs):
#     if sender.name == 'paperless_kafka':
#        initialize_kafka_producer_task()
