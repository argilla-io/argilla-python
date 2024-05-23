from argilla_sdk.records._io._generic import GenericIOMixin  # noqa
from argilla_sdk.records._io._json import JSONIOMixin  # noqa


class RecordsIOMixin(GenericIOMixin, JSONIOMixin):
    pass
