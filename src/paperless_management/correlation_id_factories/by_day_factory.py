from .correlation_id_abstract import CorrelationIdAbstract
from datetime import datetime
from paperless_management import constants

class ByDayFactory(CorrelationIdAbstract):
    def _generate_batch(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime(constants.YYYYMMDD_DATE_FORMAT)
        self._batch = f"{self._batch_keyword}{formatted_date}"
        return self._batch

    def _generate_document_index(self):
        stringified_doc_index = constants.ONE_LABEL

        if (
            self._previous_correlation_id is not None
            and self._previous_correlation_id.batch == self._batch
        ):
            stringified_doc_index = str(
                int(self._previous_correlation_id.document_index) + 1
            )

        while len(stringified_doc_index) < constants.DOCUMENTS_INDEX_MAX_LENGTH:
            stringified_doc_index = constants.ZERO_LABEL + stringified_doc_index

        return stringified_doc_index
