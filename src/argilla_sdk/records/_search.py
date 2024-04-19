from typing import Optional, List, Any, Union, Tuple, NamedTuple

from argilla_sdk._models import SearchQueryModel
from argilla_sdk._models._search import (
    TextQueryModel,
    ResponseFilterScopeModel,
    SuggestionFilterScopeModel,
    MetadataFilterScopeModel,
    ScopeModel,
    RangeFilterModel,
    TermsFilterModel,
    FilterModel,
    AndFilterModel,
)


class Condition(Tuple[str, str, Any]):

    """This class is used to map user conditions to the internal filter models"""

    @property
    def model(self) -> FilterModel:
        field, operator, value = self

        field = field.strip()
        scope = self._extract_filter_scope(field)

        operator = operator.strip()
        if operator == "==":
            return TermsFilterModel(values=[value], scope=scope)
        elif operator == "in":
            return TermsFilterModel(values=value, scope=scope)
        elif operator in [">="]:
            return RangeFilterModel(ge=value, scope=scope)
        elif operator == "<=":
            return RangeFilterModel(le=value, scope=scope)
        else:
            raise ValueError(f"Unknown operator: {operator}")

    @staticmethod
    def _extract_filter_scope(field: str) -> ScopeModel:
        field = field.strip()

        if field == "status":
            return ResponseFilterScopeModel(property="status")
        elif "metadata" in field:
            _, md_property = field.split(".")
            return MetadataFilterScopeModel(metadata_property=md_property)
        elif "suggestion" in field:
            question, _ = field.split(".")
            return SuggestionFilterScopeModel(question=question)
        elif "score" in field:
            question, _ = field.split(".")
            return SuggestionFilterScopeModel(question=question, property="score")
        elif "response" in field:
            question, _ = field.split(".")
            return ResponseFilterScopeModel(question=question)
        else:  # Question field -> Suggestion
            return SuggestionFilterScopeModel(question=field)


class Filter:
    """This class is used to map user filters to the internal filter models"""

    def __init__(self, conditions: Union[List[Tuple[str, str, Any]], Tuple[str, str, Any], None] = None):
        if isinstance(conditions, tuple):
            conditions = [conditions]
        self.conditions = [Condition(condition) for condition in conditions]

    @property
    def model(self) -> AndFilterModel:
        return AndFilterModel.parse_obj({"and": [condition.model for condition in self.conditions]})


class Query:
    """This class is used to map user queries to the internal query models"""

    query: Optional[str] = None

    def __init__(self, *, query: Union[str, None] = None, filters: Union[List[Filter], Filter, None] = None):
        if isinstance(filters, Filter):
            filters = [filters]

        self.query = query
        self.filters = filters

    @property
    def model(self) -> SearchQueryModel:
        model = SearchQueryModel()

        if self.query is not None:
            model.query = TextQueryModel(q=self.query)

        if self.filters:
            model.filters = self.filters[0].model

        return model


__all__ = ["Query", "Filter", "Condition"]
