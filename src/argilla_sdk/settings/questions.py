from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, validator, field_serializer


class QuestionSettings(BaseModel):
    type: str


class TextQuestionSettings(QuestionSettings):
    use_markdown: bool = False


class LabelQuestionSettings(QuestionSettings):
    type: str = "label_selection"
    options: List[str] = []


class QuestionBase(BaseModel):
    name: str
    settings: QuestionSettings

    id: UUID = uuid4()
    title: Optional[str] = None
    description: Optional[str] = None
    required: bool = True
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        validate_assignment = True

    @validator("name")
    def __name_lower(cls, name):
        formatted_name = name.lower().replace(" ", "_")
        return formatted_name

    @validator("title", always=True)
    def __title_default(cls, title, values):
        validated_title = title or values["name"]
        return validated_title

    @validator("description", always=True)
    def __description_default(cls, description, values):
        validated_description = description or values["title"]
        return validated_description

    @field_serializer("inserted_at", "updated_at", when_used="unless-none")
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("id", when_used="unless-none")
    def serialize_id(self, value: UUID) -> str:
        return str(value)


class LabelQuestion(QuestionBase):
    labels: List[str]
    settings: LabelQuestionSettings = LabelQuestionSettings(type="label_selection")


class RatingQuestion(QuestionBase):
    values: List[int]
    settings: QuestionSettings = QuestionSettings(type="rating")


class TextQuestion(QuestionBase):
    use_markdown: bool = False
    settings: TextQuestionSettings = TextQuestionSettings(type="text")

    @validator("settings", pre=True, always=True)
    def __move_use_markdown(cls, settings, values):
        use_markdown = values.get("use_markdown", False)
        settings.use_markdown = use_markdown
        return settings


class MultiLabelQuestion(QuestionBase):
    labels: List[str]
    visible_labels: int
    settings: QuestionSettings = QuestionSettings(type="multi_label_selection")


class RankingQuestion(QuestionBase):
    values: List[int]
    settings: QuestionSettings = QuestionSettings(type="ranking")
