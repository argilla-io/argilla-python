from typing import Any, Optional, Literal, Union, List
from uuid import UUID, uuid4

from pydantic import BaseModel, field_serializer


class SuggestionModel(BaseModel):
    """Schema for the suggestions for the questions related to the record."""

    value: Any

    question_name: Optional[str] = None
    type: Optional[Literal["model", "human"]] = None
    score: Union[float, List[float], None] = None
    agent: Optional[str] = None
    id: Optional[UUID] = uuid4()
    question_id: Optional[UUID] = None

    @field_serializer("id", when_used="unless-none")
    def serialize_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer("question_id", when_used="unless-none")
    def serialize_question_id(self, value: UUID) -> str:
        return str(value)
