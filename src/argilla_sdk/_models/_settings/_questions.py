from datetime import datetime
from typing import Dict, List, Optional, Union, ClassVar
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator, Field, model_validator
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Self


class QuestionSettings(BaseModel, validate_assignment=True):
    type: str


class TextQuestionSettings(QuestionSettings):
    type: str = "text"

    use_markdown: bool = False


class RatingQuestionSettings(QuestionSettings):
    type: str = "rating"

    options: List[dict] = Field(..., validate_default=True)

    @field_validator("options", mode="before")
    @classmethod
    def __values_are_unique(cls, options: List[dict]) -> List[dict]:
        """Ensure that values are unique"""

        unique_values = list(set([option["value"] for option in options]))
        if len(unique_values) != len(options):
            raise ValueError("All values must be unique")

        return options


class LabelQuestionSettings(QuestionSettings):
    type: str = "label_selection"

    _MIN_VISIBLE_OPTIONS: ClassVar[int] = 3

    options: List[Dict[str, Optional[str]]] = Field(default_factory=list, validate_default=True)
    visible_options: Optional[int] = Field(None, validate_default=True, ge=_MIN_VISIBLE_OPTIONS)

    @field_validator("options", mode="before")
    @classmethod
    def __labels_are_unique(cls, options: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
        """Ensure that labels are unique"""

        unique_labels = list(set([option["value"] for option in options]))
        if len(unique_labels) != len(options):
            raise ValueError("All labels must be unique")
        return options

    @model_validator(mode="after")
    def __validate_visible_options(self) -> "Self":
        if self.visible_options is None and self.options and len(self.options) >= self._MIN_VISIBLE_OPTIONS:
            self.visible_options = len(self.options)
        return self


class MultiLabelQuestionSettings(LabelQuestionSettings):
    type: str = "multi_label_selection"


class RankingQuestionSettings(QuestionSettings):
    type: str = "ranking"

    options: List[Dict[str, Optional[str]]] = Field(default_factory=list, validate_default=True)

    @field_validator("options", mode="before")
    @classmethod
    def __values_are_unique(cls, options: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
        """Ensure that values are unique"""

        unique_values = list(set([option["value"] for option in options]))
        if len(unique_values) != len(options):
            raise ValueError("All values must be unique")

        return options


class SpanQuestionSettings(QuestionSettings):
    type: str = "span"

    _MIN_VISIBLE_OPTIONS: ClassVar[int] = 3

    allow_overlapping: bool = False
    field: Optional[str] = None
    options: List[Dict[str, Optional[str]]] = Field(default_factory=list, validate_default=True)
    visible_options: Optional[int] = Field(None, validate_default=True, ge=_MIN_VISIBLE_OPTIONS)

    @field_validator("options", mode="before")
    @classmethod
    def __values_are_unique(cls, options: List[Dict[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
        """Ensure that values are unique"""

        unique_values = list(set([option["value"] for option in options]))
        if len(unique_values) != len(options):
            raise ValueError("All values must be unique")

        return options

    @model_validator(mode="after")
    def __validate_visible_options(self) -> "Self":
        if self.visible_options is None and self.options and len(self.options) >= self._MIN_VISIBLE_OPTIONS:
            self.visible_options = len(self.options)
        return self


class QuestionBaseModel(BaseModel, validate_assignment=True):
    id: Optional[UUID] = None
    name: str
    settings: QuestionSettings

    title: str = Field(None, validate_default=True)
    description: Optional[str] = Field(None, validate_default=True)
    required: bool = True
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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
    settings: LabelQuestionSettings


class RatingQuestionModel(QuestionBaseModel):
    settings: RatingQuestionSettings


class TextQuestionModel(QuestionBaseModel):
    settings: TextQuestionSettings


class MultiLabelQuestionModel(LabelQuestionModel):
    settings: MultiLabelQuestionSettings


class RankingQuestionModel(QuestionBaseModel):
    settings: RankingQuestionSettings


class SpanQuestionModel(QuestionBaseModel):
    settings: SpanQuestionSettings


QuestionModel = Union[
    LabelQuestionModel,
    RatingQuestionModel,
    TextQuestionModel,
    MultiLabelQuestionModel,
    RankingQuestionModel,
    QuestionBaseModel,
]
