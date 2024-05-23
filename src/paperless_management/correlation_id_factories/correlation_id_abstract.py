from paperless_management import constants

class CorrelationIdAbstract:
    _batch_keyword = ""
    _previous_correlation_id = ""
    _batch = ""

    def __init__(self, config, previous_correlation_id):
        self._batch_keyword = config[constants.BATCH_KEYWORD_LABEL]
        self._previous_correlation_id = previous_correlation_id

    def _generate_batch(self):
        pass

    def _generate_document_index(self):
        pass
