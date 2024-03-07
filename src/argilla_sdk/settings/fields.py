from pydantic import BaseModel, validator

from typing import Optional

from argilla_sdk._helpers._log import log
from argilla_sdk.settings.exceptions import InvalidFieldException

class FieldSettings(BaseModel):
    type: str
    use_markdown: Optional[bool] = False


class TextField(BaseModel):
    name: str
    title: Optional[str] = None
    required: bool = True
    settings: FieldSettings = FieldSettings(type="text")
    use_markdown: Optional[bool] = None

    @validator("name")
    def __name_lower(cls, name):
        formatted_name = name.lower().replace(" ", "_")
        if len(formatted_name) == 0:
            raise InvalidFieldException(f"Name have characters. Got {formatted_name}")
        if not any(char.isalpha() for char in formatted_name):
            raise InvalidFieldException(f"Name must contain at least one letter. Got {formatted_name}")
        log(f"Formatted TextField name to {formatted_name}")
        return formatted_name

    @validator("title", always=True)
    def __title_default(cls, title, values):
        validated_title = title or values["name"]
        log(f"TextField title is {validated_title}")
        return validated_title
