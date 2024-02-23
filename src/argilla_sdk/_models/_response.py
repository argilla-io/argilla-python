from enum import Enum
from typing import Dict, Optional, Union
from uuid import UUID
import warnings

from pydantic import BaseModel, validator


class ResponseStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    discarded = "discarded"


class ResponseModel(BaseModel):
    """Schema for the `FeedbackRecord` response."""

    user_id: Optional[UUID] = None
    values: Union[Dict[str, str], None]
    status: ResponseStatus = ResponseStatus.submitted

    class Config:
        validate_assignment = True

    @validator("user_id", always=True)
    def user_id_must_have_value(cls, v):
        if not v:
            warnings.warn(
                "`user_id` not provided, so it will be set to `None`. Which is not an"
                " issue, unless you're planning to log the response in Argilla, as"
                " it will be automatically set to the active `user_id`.",
            )
        return v
