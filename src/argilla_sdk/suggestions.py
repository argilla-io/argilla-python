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

from typing import Any, Optional, Literal, Union, List
from uuid import UUID

from argilla_sdk._models import SuggestionModel
from argilla_sdk._resource import Resource

__all__ = ["Suggestion"]


class Suggestion(Resource):
    _model: SuggestionModel

    def __init__(
        self,
        question_name: str,
        value: Any,
        type: Optional[Literal["model", "human"]] = None,
        score: Union[float, List[float], None] = None,
        agent: Optional[str] = None,
        id: Optional[UUID] = None,
        question_id: Optional[UUID] = None,
    ) -> None:
        self._model = SuggestionModel(
            value=value,
            question_name=question_name,
            type=type,
            score=score,
            agent=agent,
            id=id,
            question_id=question_id,
        )

    @property
    def value(self) -> Any:
        return self._model.value

    # TODO: Add getter and setter at question type level
    #  @property
    #  def question(self) -> Optional["QuestionType"]:
    #      pass
    #  @question.setter
    #  def question(self, value: "QuestionType") -> None:
    #      self._model.question_name = value.name
    #      self._model.question_id = value.id

    @property
    def question_name(self) -> str:
        return self._model.question_name

    @question_name.setter
    def question_name(self, value: str) -> None:
        self._model.question_name = value

    @property
    def question_id(self) -> Optional[UUID]:
        return self._model.question_id

    @question_id.setter
    def question_id(self, value: UUID) -> None:
        self._model.question_id = value

    @property
    def type(self) -> Optional[Literal["model", "human"]]:
        return self._model.type

    @property
    def score(self) -> Optional[Union[float, List[float]]]:
        return self._model.score

    @score.setter
    def score(self, value: float) -> None:
        self._model.score = value

    @property
    def agent(self) -> Optional[str]:
        return self._model.agent

    @agent.setter
    def agent(self, value: str) -> None:
        self._model.agent = value

    @property
    def question_id(self) -> Optional[UUID]:
        return self._model.question_id

    @classmethod
    def from_model(cls, model: SuggestionModel) -> "Suggestion":
        return cls(**model.model_dump())
