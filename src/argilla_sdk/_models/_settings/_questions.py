from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator, Field
from pydantic_core.core_schema import ValidationInfo


class QuestionSettings(BaseModel):
    type: str


class TextQuestionSettings(QuestionSettings):
    use_markdown: bool = False


class LabelQuestionSettings(QuestionSettings):
    type: str = "label_selection"
    options: List[Dict[str, Optional[str]]] = Field(default_factory=list, validate_default=True)

    @field_validator("options", mode="before")
    @classmethod
    def __labels_are_unique(cls, labels: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
        """Ensure that labels are unique"""

        unique_labels = list(set([label["value"] for label in labels]))
        if len(unique_labels) != len(labels):
            raise ValueError("All labels must be unique")
        return labels


class SpanQuestionSettings(QuestionSettings):
    type: str = "span"

    allow_overlapping: bool = False
    field: Optional[str] = None
    options: List[Dict[str, Optional[str]]] = Field(default_factory=list, validate_default=True)
    visible_options: Optional[int] = Field(None, validate_default=True)

    @field_validator("visible_options", mode="before")
    @classmethod
    def __default_to_all(cls, visible_labels: Optional[int], info) -> int:
        data = info.data
        if visible_labels is None and data["options"]:
            return len(data["options"])
        return visible_labels

    @field_validator("options", mode="before")
    @classmethod
    def __options_are_unique(cls, options: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
        """Ensure that labels are unique"""

        unique_options = list(set([label["value"] for label in options]))
        if len(unique_options) != len(options):
            raise ValueError("All labels must be unique")
        return options


class QuestionBaseModel(BaseModel):
    id: Optional[UUID] = None
    name: str
    settings: QuestionSettings

    title: str = Field(None, validate_default=True)
    description: Optional[str] = Field(None, validate_default=True)
    required: bool = True
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        validate_assignment = True

    @field_validator("name")
    @classmethod
    def __name_lower(cls, name: str, info: ValidationInfo):
        formatted_name = name.lower().replace(" ", "_")
        return formatted_name

    @field_validator("title", mode="before")
    @classmethod
    def __title_default(cls, title, info: ValidationInfo):
        validated_title = title or info.data["name"]
        return validated_title

    @field_validator("description")
    @classmethod
    def __description_default(cls, description, info: ValidationInfo) -> Optional[str]:
        data = info.data
        return description or data["title"]

    @field_serializer("inserted_at", "updated_at", when_used="unless-none")
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("id", when_used="unless-none")
    def serialize_id(self, value: UUID) -> str:
        return str(value)


class LabelQuestionModel(QuestionBaseModel):
    settings: LabelQuestionSettings = LabelQuestionSettings(type="label_selection")


class RatingQuestionModel(QuestionBaseModel):
    values: List[int]
    settings: QuestionSettings = QuestionSettings(type="rating")


class TextQuestionModel(QuestionBaseModel):
    use_markdown: bool = False
    settings: TextQuestionSettings = Field(TextQuestionSettings(type="text"), validate_default=True)

    @field_validator("settings", mode="before")
    @classmethod
    def __move_use_markdown(cls, _, info: ValidationInfo):
        data = info.data
        use_markdown = data.get("use_markdown", False)
        return TextQuestionSettings(type="text", use_markdown=use_markdown)


class MultiLabelQuestionModel(LabelQuestionModel):
    visible_labels: Optional[int] = Field(None, validate_default=True)
    settings: QuestionSettings = LabelQuestionSettings(type="multi_label_selection")

    @field_validator("visible_labels")
    @classmethod
    def __default_to_all(cls, visible_labels, values) -> int:
        if visible_labels is None:
            return len(values["labels"])
        return visible_labels


class RankingQuestionModel(QuestionBaseModel):
    values: List[int]
    settings: QuestionSettings = QuestionSettings(type="ranking")


class SpanQuestionModel(QuestionBaseModel):
    settings: SpanQuestionSettings = Field(default_factory=SpanQuestionSettings)


QuestionModel = Union[
    LabelQuestionModel,
    RatingQuestionModel,
    TextQuestionModel,
    MultiLabelQuestionModel,
    RankingQuestionModel,
    QuestionBaseModel,
]
