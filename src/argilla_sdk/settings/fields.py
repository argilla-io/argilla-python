from pydantic import BaseModel, validator

from typing import Optional


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
        return formatted_name

    @validator("title", always=True)
    def __title_default(cls, title, values):
        validated_title = title or values["name"]
        return validated_title

    @validator("settings", pre=True, always=True)
    def __move_use_markdown(cls, settings, values):
        use_markdown = values.get("use_markdown", False)
        settings.use_markdown = use_markdown
        return settings
