# from celery import shared_task
# from .kafka_producer import KafkaProducerSingleton
#
#
# @shared_task
# def initialize_kafka_producer_task():
#     kafka_producer = KafkaProducerSingleton()
#     try:
#         # Perform any necessary initialization actions
#         pass
#     finally:
#         kafka_producer.cleanup()
#
