from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator, Field
from pydantic_core.core_schema import ValidationInfo

from argilla_sdk._helpers._log import log


class FieldSettings(BaseModel):
    type: str = Field(validate_default=True)
    use_markdown: Optional[bool] = False


class FieldBaseModel(BaseModel):
    id: Optional[UUID] = None
    name: str

    title: Optional[str] = None
    required: bool = True
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def __name_lower(cls, name):
        formatted_name = name.lower().replace(" ", "_")
        return formatted_name

    @field_validator("title")
    @classmethod
    def __title_default(cls, title: str, info: ValidationInfo) -> str:
        data = info.data
        validated_title = title or data["name"]
        log(f"TextField title is {validated_title}")
        return validated_title

    @field_serializer("id", when_used="unless-none")
    def serialize_id(self, value: UUID) -> str:
        return str(value)


class TextFieldModel(FieldBaseModel):
    settings: FieldSettings = FieldSettings(type="text", use_markdown=False)


class VectorFieldModel(FieldBaseModel):
    dimensions: int
    settings: Optional[FieldSettings] = FieldSettings(type="vector")

    @field_validator("dimensions")
    @classmethod
    def __dimension_gt_zero(cls, dimensions):
        if dimensions <= 0:
            raise ValueError("dimensions must be greater than 0")
        return dimensions


FieldModel = Union[TextFieldModel, VectorFieldModel]
