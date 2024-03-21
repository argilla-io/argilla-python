from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import Field, field_serializer

from argilla_sdk._models._resource import ResourceModel
from argilla_sdk._models._response import ResponseModel
from argilla_sdk._models._suggestion import SuggestionModel


class RecordModel(ResourceModel):
    """Schema for the records of a `Dataset`"""

    fields: Dict[str, Union[str, None]]
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    vectors: Optional[Dict[str, List[float]]] = Field(default_factory=dict)
    responses: Optional[List[ResponseModel]] = Field(default_factory=list)
    suggestions: Optional[Union[Tuple[SuggestionModel], List[SuggestionModel]]] = Field(default_factory=tuple)
    external_id: Optional[Any] = None

    @field_serializer("external_id", when_used="unless-none")
    def serialize_external_id(self, value: str) -> str:
        return str(value)
