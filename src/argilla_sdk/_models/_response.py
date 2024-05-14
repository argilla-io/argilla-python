import warnings
from enum import Enum
from typing import Dict, Optional, Union, Any
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator, Field


class ResponseStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    discarded = "discarded"


class UserResponseModel(BaseModel):
    """Schema for the `FeedbackRecord` user response."""

    values: Union[Dict[str, Dict[str, Any]], None]
    status: ResponseStatus
    user_id: Optional[UUID] = Field(None, validate_default=True)

    class Config:
        validate_assignment = True

    @field_validator("user_id")
    @classmethod
    def user_id_must_have_value(cls, user_id: Optional[UUID]):
        if not user_id:
            warnings.warn(
                "`user_id` not provided, so it will be set to `None`. Which is not an"
                " issue, unless you're planning to log the response in Argilla, as"
                " it will be automatically set to the active `user_id`.",
            )
        return user_id

    @field_serializer("user_id", when_used="always")
    def serialize_user_id(value: UUID) -> str:
        return str(value)
