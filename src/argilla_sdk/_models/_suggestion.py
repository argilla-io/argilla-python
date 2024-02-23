from typing import Any, Optional, Literal

from pydantic import BaseModel


class SuggestionModel(BaseModel):
    """Schema for the suggestions for the questions related to the record."""

    question_name: str
    type: Optional[Literal["model", "human"]] = None
    score: Optional[float] = None
    value: Any
    agent: Optional[str] = None
