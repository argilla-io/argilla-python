from typing import List, Optional

from argilla_sdk.settings.fields import FieldBase
from argilla_sdk.settings.questions import QuestionBase
from argilla_sdk.settings.guidelines import Guidelines


class Settings:
    def __init__(
        self,
        fields: Optional[List[FieldBase]] = None,
        questions: Optional[List[QuestionBase]] = None,
        guidelines: Optional[str] = None,
    ):
        self.__guidelines = self.__process_guidelines(guidelines)
        self.__fields = self.__process_fields(fields) or []
        self.__questions = self.__process_questions(questions) or []

    ############################
    # Property methods         #
    ############################

    @property
    def guidelines(
        self,
    ) -> None:
        return self.__guidelines.guidelines

    @guidelines.setter
    def guidelines(self, guidelines: str) -> None:
        self.__guidelines = self.__process_guidelines(guidelines)

    @property
    def fields(
        self,
    ) -> None:
        return self.__fields

    @fields.setter
    def fields(self, fields: List[FieldBase]) -> None:
        self.__fields = self.__process_fields(fields)

    @property
    def questions(
        self,
    ) -> None:
        return self.__questions

    @questions.setter
    def questions(self, questions: List[FieldBase]) -> None:
        self.__questions = self.__process_questions(questions)

    ############################
    # Utility Methods          #
    ############################

    def __process_fields(self, fields):
        return fields

    def __process_questions(self, questions):
        return questions

    def __process_guidelines(self, guidelines):
        return Guidelines(guidelines)

    def serialize(self):
        return {
            "guidelines": self.__guidelines.serialize() if self.__guidelines else None,
            "fields": [field.serialize() for field in self.__fields],
            "questions": [question.serialize() for question in self.__questions],
        }
