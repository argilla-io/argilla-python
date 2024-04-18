from typing import List, Any, Union, Literal, Annotated

from pydantic import BaseModel, Field


class ResponseFilterScopeModel(BaseModel):
    """Filter scope for filtering on a response entity."""

    entity: Literal["response"] = "response"
    question: Union[str, None] = None
    property: Union[Literal["status"], None] = None


class SuggestionFilterScopeModel(BaseModel):
    """Filter scope for filtering on a suggestion entity."""

    entity: Literal["suggestion"] = "suggestion"
    question: str
    property: Union[Literal["value"], Literal["agent"], Literal["score"], None] = "value"


class MetadataFilterScopeModel(BaseModel):
    """Filter scope for filtering on a metadata entity."""

    entity: Literal["metadata"] = "metadata"
    metadata_property: str


Scope = Annotated[
    Union[ResponseFilterScopeModel, SuggestionFilterScopeModel, MetadataFilterScopeModel,],
    Field(discriminator="entity"),
]


class TermsFilterModel(BaseModel):
    """Filter model for terms filter."""

    type: Literal["terms"] = "terms"
    values: List[str]
    scope: Scope


class RangeFilterModel(BaseModel):
    """Filter model for range filter."""
    type: Literal["range"] = "range"
    ge: Any
    le: Any
    scope: Scope


FilterModel = Annotated[
    Union[TermsFilterModel, RangeFilterModel,],
    Field(discriminator="type")
]


class AndFilterModel(BaseModel):
    """And filter model."""
    and_: List[FilterModel] = Field(alias="and")


class TextQueryModel(BaseModel):
    """Text query model."""
    q: str
    field: Union[str, None] = None


class QueryModel(BaseModel):
    """Query part of the search query model"""
    text: TextQueryModel


class SearchQueryModel(BaseModel):
    """The main search query model."""
    query: Union[QueryModel, None] = None
    filters: Union[AndFilterModel, None] = None
