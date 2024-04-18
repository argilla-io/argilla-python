from typing import Optional, List, Tuple, Union

from argilla_sdk._models import SearchQueryModel
from argilla_sdk._models._search import (
    TextQueryModel,
    AndFilterModel,
    FilterModel,
    SuggestionFilterScopeModel,
    ResponseFilterScopeModel,
    TermsFilterModel,
    RangeFilterModel,
)

__all__ = ["Query"]


class Query:
    """This class is used to map user queries to the internal query models"""

    query: Optional[str] = None
    filters: Optional[List[dict]] = None

    def __init__(self, *, query: Optional[str] = None, filters: Optional[List[Tuple[str, dict]]] = None):
        self.query = query
        self.filters = filters

    @property
    def model(self) -> SearchQueryModel:
        model = SearchQueryModel()

        if self.query is not None:
            model.query = TextQueryModel(q=self.query)
        if self.filters:
            model.filters = AndFilterModel.parse_obj(
                {"and": [self._parse_filter(key, filter) for key, filter in self.filters]}
            )

        return model

    def _parse_filter(self, key: str, filter: dict) -> FilterModel:
        entity, prop = self._split_filter_key(key)

        if entity == "suggestion":
            scope = SuggestionFilterScopeModel(question=filter["question"], property=prop)
        elif entity == "response":
            scope = ResponseFilterScopeModel(question=filter.get("question"), property=prop)
        else:  # pragma: no cover
            raise ValueError(f"Unknown filter entity: {entity}")

        if "terms" in filter:
            return TermsFilterModel(values=filter["terms"], scope=scope)
        elif "range" in filter:
            return RangeFilterModel(**filter["range"], scope=scope)
        else:  # pragma: no cover
            raise ValueError(f"Unknown filter type: {filter}")

    @staticmethod
    def _split_filter_key(key) -> Tuple[str, Union[str, None]]:
        key_parts = key.split(".")
        entity = key_parts[0]
        prop = None

        if len(key_parts) > 1:
            prop = key_parts[1]

        return entity, prop
