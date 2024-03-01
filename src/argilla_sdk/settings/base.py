from typing import List, Optional, Union

from pydantic import BaseModel, validator

from argilla_sdk.settings.fields import TextField
from argilla_sdk.settings.questions import (
    LabelQuestion,
    MultiLabelQuestion,
    RankingQuestion,
    TextQuestion,
    RatingQuestion,
)


class Settings(BaseModel):
    """Settings class for Argilla Datasets. This class is used to define the representation of a Dataset within the UI.
    Args:
        guidelines (str): A string containing the guidelines for the Dataset.
        fields (List[TextField]): A list of TextField objects that represent the fields in the Dataset.
        questions (List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion, RatingQuestion]]): A list of Question objects that represent the questions in the Dataset.
        allow_extra_metadata (bool): A boolean that determines whether or not extra metadata is allowed in the Dataset. Defaults to False.
    """

    fields: Optional[List[TextField]] = []
    questions: Optional[
        List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion, RatingQuestion]]
    ] = []
    guidelines: Optional[str] = None
    allow_extra_metadata: bool = False

    class Config:
        validate_assignment = True

    @validator("fields", each_item=True)
    def __process_fields(cls, value: Union[TextField, dict]) -> TextField:
        if isinstance(value, dict):
            return TextField(**value)
        return value

    @validator("questions", each_item=True)
    def __process_questions(cls, value):
        # TODO: process questions to be of type LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion
        return value

    @validator("guidelines", always=True)
    def __process_guidelines(cls, value):
        # TODO: process guidelines to be of type str or load str from file
        return value

    def serialize(self):
        return {
            "guidelines": self.guidelines,
            "fields": [field.model_dump() for field in self.fields],
            "questions": [question.model_dump() for question in self.questions],
            "allow_extra_metadata": self.allow_extra_metadata,
        }
