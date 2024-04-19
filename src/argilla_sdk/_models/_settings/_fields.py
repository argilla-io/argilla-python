from uuid import UUID

from pydantic import BaseModel, validator

from typing import Optional

from argilla_sdk._helpers._log import log


class FieldSettings(BaseModel):
    type: str
    use_markdown: Optional[bool] = False


class FieldBaseModel(BaseModel):
    id: Optional[UUID] = None
    name: str
    settings: FieldSettings

    title: Optional[str] = None
    required: bool = True
    description: Optional[str] = None

    @validator("name")
    def __name_lower(cls, name):
        formatted_name = name.lower().replace(" ", "_")
        return formatted_name

    @validator("title", always=True)
    def __title_default(cls, title, values):
        validated_title = title or values["name"]
        log(f"TextField title is {validated_title}")
        return validated_title


class TextFieldModel(FieldBaseModel):
    settings: FieldSettings = FieldSettings(type="text", use_markdown=False)


FieldModel = TextFieldModel
