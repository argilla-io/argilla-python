# Copyright 2024-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional, Union, TYPE_CHECKING

from argilla_sdk._models import SettingsModel
from argilla_sdk._resource import Resource
from argilla_sdk._models import (
    TextFieldModel,
    LabelQuestionModel,
    MultiLabelQuestionModel,
    RankingQuestionModel,
    TextQuestionModel,
    RatingQuestionModel,
)

if TYPE_CHECKING:
    from argilla_sdk.settings import (
        TextField,
        LabelQuestion,
        MultiLabelQuestion,
        RankingQuestion,
        TextQuestion,
        RatingQuestion,
    )


__all__ = ["Settings"]

SettingsModel.model_rebuild()


class Settings(Resource):
    """Settings class for Argilla Datasets. This class is used to define the representation of a Dataset within the UI."""

    _model: SettingsModel

    def __init__(
        self,
        fields: Optional[List[TextFieldModel]] = [],
        questions: Optional[
            List[
                Union[
                    LabelQuestionModel,
                    MultiLabelQuestionModel,
                    RankingQuestionModel,
                    TextQuestionModel,
                    RatingQuestionModel,
                ]
            ]
        ] = [],
        guidelines: Optional[str] = None,
        allow_extra_metadata: bool = False,
    ) -> None:
        """
        Args:
            guidelines (str): A string containing the guidelines for the Dataset.
            fields (List[TextField]): A list of TextField objects that represent the fields in the Dataset.
            questions (List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion, RatingQuestion]]): A list of Question objects that represent the questions in the Dataset.
            allow_extra_metadata (bool): A boolean that determines whether or not extra metadata is allowed in the Dataset. Defaults to False.
        """
        self._model = SettingsModel(
            fields=self.__process_fields(fields),
            questions=self.__process_questions(questions),
            guidelines=self.__process_guidelines(guidelines),
            allow_extra_metadata=allow_extra_metadata,
        )
        self.fields = fields
        self.questions = questions
        self.guidelines = guidelines
        self.allow_extra_metadata = allow_extra_metadata

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, fields):
        self._model.fields = self.__process_fields(fields)
        self.__fields = fields

    @property
    def questions(
        self,
    ) -> List[
        Union[LabelQuestionModel, MultiLabelQuestionModel, RankingQuestionModel, TextQuestionModel, RatingQuestionModel]
    ]:
        return self.__questions

    @questions.setter
    def questions(
        self,
        questions=List[
            Union[
                "LabelQuestion",
                "MultiLabelQuestion",
                "RankingQuestion",
                "TextQuestion",
                "RatingQuestion",
            ]
        ],
    ):
        self._model.questions = self.__process_questions(questions)
        self.__questions = questions

    @property
    def guidelines(self):
        return self.__guidelines

    @guidelines.setter
    def guidelines(self, guidelines):
        self._model.guidelines = self.__process_guidelines(guidelines)
        self.__guidelines = guidelines

    @property
    def allow_extra_metadata(self):
        return self.__allow_extra_metadata

    @allow_extra_metadata.setter
    def allow_extra_metadata(self, value):
        self._model._allow_extra_metadata = value
        self.__allow_extra_metadata = value

    def serialize(self):
        return {
            "guidelines": self.guidelines,
            "fields": self.__serialize_fields(fields=self.fields),
            "questions": self.__serialize_questions(questions=self.questions),
            "allow_extra_metadata": self.allow_extra_metadata,
        }

    ### Utility Methods ###

    def __process_fields(self, fields: List["TextField"]) -> List["TextField"]:
        processed_fields = [field._model for field in fields]
        return processed_fields

    def __process_questions(self, questions) -> List["TextQuestion"]:
        processed_questions = [question._model for question in questions]
        return processed_questions

    def __process_guidelines(self, value):
        # TODO: process guidelines to be of type str or load str from file
        return value

    def __serialize_fields(self, fields):
        return [field.serialize() for field in fields]

    def __serialize_questions(self, questions):
        return [question.serialize() for question in questions]
