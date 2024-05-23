from . import constants
from .models import CorrelationId
from paperless_management.correlation_id_factories.correlation_id_factory \
    import CorrelationIdFactory
from paperless_management import constants as management_constants
import logging

logger = logging.getLogger("documents")


class CorrelationIdService:
    _correlation_id = ""
    _batch = ""
    _flow_type = ""
    _document_index = ""
    _activity = ""

    def __init__(self, document_config, activity,
                 flow_type=constants.NUMERIC_FLOW_LABEL, ):
        self._activity = activity
        self._flow_type = flow_type

        previous_correlation_id = self._get_previous_correlation_id()
        correlation_id_factory = CorrelationIdFactory(document_config,
                                                      previous_correlation_id)
        self._batch = correlation_id_factory._generate_batch()
        self._document_index = (
            correlation_id_factory._generate_document_index())
        self._correlation_id = self._build_correlation_id()

    def _get_previous_correlation_id(self):
        try:
            return CorrelationId.objects.get(activity=self._activity)
        except Exception:
            return None

    def save_correlation_id(self):
        CorrelationId.objects.update_or_create(activity=self._activity,
                                               defaults={
                                                   "activity": self._activity,
                                                   "batch": self._batch,
                                                   "document_index":
                                                       self._document_index,
                                                   }, )

    def _build_correlation_id(self):
        return constants.CORRELATION_ID_FORMAT(self._activity, self._batch,
                                               self._flow_type,
                                               self._document_index)

    def get_correlation_id(self):
        return self._correlation_id
