from typing import List, Optional, Union

from attr import dataclass

from argilla_sdk.settings.fields import TextField
from argilla_sdk.settings.questions import LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion


@dataclass
class Settings:
    _fields: Optional[List[TextField]] = []
    _questions: Optional[List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion]]] = []
    _guidelines: Optional[str] = None
    _allow_extra_metadata: bool = False

    ############################
    # Property methods         #
    ############################

    @property
    def guidelines(
        self,
    ) -> Union[str, None]:
        return self._guidelines

    @guidelines.setter
    def guidelines(self, guidelines: str) -> None:
        self._guidelines = self.__process_guidelines(guidelines=guidelines)

    @property
    def fields(
        self,
    ) -> List[TextField]:
        return self._fields

    @fields.setter
    def fields(self, fields: List[TextField]) -> None:
        self._fields = self.__process_fields(fields=fields)

    @property
    def questions(
        self,
    ) -> List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion]]:
        return self._questions

    @questions.setter
    def questions(
        self, questions: List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion]]
    ) -> None:
        self._questions = self.__process_questions(questions=questions)

    @property
    def allow_extra_metadata(
        self,
    ) -> bool:
        return self._allow_extra_metadata

    ############################
    # Utility Methods          #
    ############################

    def __process_fields(self, fields):
        return fields

    def __process_questions(self, questions):
        return questions

    def __process_guidelines(self, guidelines):
        return guidelines

    def serialize(self):
        return {
            "guidelines": self._guidelines,
            "fields": [field.serialize() for field in self._fields],
            "questions": [question.serialize() for question in self._questions],
        }
