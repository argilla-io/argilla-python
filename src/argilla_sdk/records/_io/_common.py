from argilla_sdk.records._io._generic import GenericExportMixin  # noqa
from argilla_sdk.records._io._json import GenericJSONIOMixin  # noqa

class RecordsIOMixin(GenericExportMixin, GenericJSONIOMixin):
    pass