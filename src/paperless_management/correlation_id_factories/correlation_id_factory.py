from paperless_management.config_management import ConfigManagement
from paperless_management import constants
from .by_day_factory import ByDayFactory


def CorrelationIdFactory(config, previous_correlation_id):
    factory = {constants.BY_DAY_FACTORY_LABEL: ByDayFactory}

    config = config if config else ConfigManagement.get_document_config(
        constants.DEFAULT_ACTIVITY_LABEL)
    previous_correlation_id = previous_correlation_id if (
        previous_correlation_id) else None

    return factory[config[constants.BATCH_TYPE_LABEL]](config,
                                                       previous_correlation_id)
