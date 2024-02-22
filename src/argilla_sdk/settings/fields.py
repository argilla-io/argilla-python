from pydantic import BaseModel, validator
from typing import Optional


class TextField(BaseModel):
    name: str
    use_markdown: bool = False
    title: Optional[str] = None
    required: bool = True

    @validator("name")
    def __name_lower(cls, name):
        return name.lower().replace(" ", "_")

    @validator("title", always=True)
    def __title_default(cls, title, values):
        return title or values["name"]
