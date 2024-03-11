from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, validator, field_serializer


class QuestionSettings(BaseModel):
    type: str
    

class TextQuestionSettings(QuestionSettings):
    use_markdown: bool = False


class LabelQuestionSettings(QuestionSettings):
    type: str = "label_selection"
    options: List[str] = []

    @validator("options", pre=True, always=True)
    def __labels_are_unique(cls, labels, values):
        """ Ensure that labels are unique """
        unique_labels = list(set(labels))
        if len(unique_labels) != len(labels):
            raise ValueError("All labels must be unique")
        return unique_labels


class QuestionBaseModel(BaseModel):
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


class LabelQuestion(QuestionBaseModel):
    labels: List[str]
    settings: LabelQuestionSettings = LabelQuestionSettings(type="label_selection")


class RatingQuestion(QuestionBaseModel):
    values: List[int]
    settings: QuestionSettings = QuestionSettings(type="rating")


class TextQuestion(QuestionBaseModel):
    use_markdown: bool = False
    settings: TextQuestionSettings = TextQuestionSettings(type="text")

    @validator("settings", pre=True, always=True)
    def __move_use_markdown(cls, settings, values):
        use_markdown = values.get("use_markdown", False)
        settings.use_markdown = use_markdown
        return settings


class MultiLabelQuestion(QuestionBaseModel):
    labels: List[str]
    visible_labels: int
    settings: QuestionSettings = QuestionSettings(type="multi_label_selection")


class RankingQuestion(QuestionBaseModel):
    values: List[int]
    settings: QuestionSettings = QuestionSettings(type="ranking")
