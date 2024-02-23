from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import Field

from argilla_sdk._models._response import ResponseModel
from argilla_sdk._models._suggestion import SuggestionModel
from argilla_sdk._models._resource import ResourceModel


class RecordModel(ResourceModel):
    """Schema for the records of a `Dataset`"""

    fields: Dict[str, Union[str, None]]
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    vectors: Optional[Dict[str, List[float]]] = Field(default_factory=dict)
    responses: Optional[List[ResponseModel]] = Field(default_factory=list)
    suggestions: Optional[Union[Tuple[SuggestionModel], List[SuggestionModel]]] = Field(default_factory=tuple)
    external_id: Optional[str] = None
