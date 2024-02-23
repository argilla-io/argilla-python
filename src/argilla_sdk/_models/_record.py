from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field

from argilla_sdk._models._response import ResponseModel
from argilla_sdk._models._suggestion import SuggestionModel


class RecordModel(BaseModel):
    """Schema for the records of a `Dataset`"""

    fields: Dict[str, Union[str, None]]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    vectors: Dict[str, List[float]] = Field(default_factory=dict)
    responses: List[ResponseModel] = Field(default_factory=list)
    suggestions: Union[Tuple[SuggestionModel], List[SuggestionModel]] = Field(default_factory=tuple)
    external_id: Optional[str] = None
