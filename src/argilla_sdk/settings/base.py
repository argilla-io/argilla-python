from typing import List, Optional, Union

from dataclasses import dataclass

from argilla_sdk.settings.fields import TextField
from argilla_sdk.settings.questions import LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion


@dataclass
class Settings:

    """Settings class for Argilla Datasets. This class is used to define the representation of a Dataset within the UI.
    Args:
        guidelines (str): A string containing the guidelines for the Dataset.
        fields (List[TextField]): A list of TextField objects that represent the fields in the Dataset.
        questions (List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion]]): A list of Question objects that represent the questions in the Dataset.
        allow_extra_metadata (bool): A boolean value that determines whether the Dataset allows for extra metadata.
    """

    fields: Optional[List[TextField]] = None
    questions: Optional[List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion]]] = None
    guidelines: Optional[str] = None
    allow_extra_metadata: bool = False

    def __post_init__(self):
        self.guidelines = self.__process_guidelines(guidelines=self.guidelines)
        self.fields = self.__process_fields(fields=self.fields)
        self.questions = self.__process_questions(questions=self.questions)

    ############################
    # Utility Methods          #
    ############################

    def __process_fields(self, fields):
        # TODO: Add validation, error handling, and processing for fields.
        return fields or []

    def __process_questions(self, questions):
        # TODO: Add validation, error handling, and processing for questions.
        return questions or []

    def __process_guidelines(self, guidelines):
        # TODO: Add validation, error handling, and processing for guidelines.
        # TODO: Add support for markdown
        return guidelines

    def serialize(self):
        return {
            "guidelines": self.guidelines,
            "fields": [field.serialize() for field in self.fields],
            "questions": [question.serialize() for question in self.questions],
        }
