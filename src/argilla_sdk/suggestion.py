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

from typing import Any, Optional, Literal
from uuid import UUID

from argilla_sdk._models import SuggestionModel
from argilla_sdk._resource import Resource

__all__ = ["Suggestion"]


class Suggestion(Resource):
    """Class for interacting with Argilla Suggestions of records"""

    _model: SuggestionModel

    def __init__(
        self,
        value: Any,
        question_name: str,
        type: Optional[Literal["model", "human"]] = None,
        score: Optional[float] = None,
        agent: Optional[str] = None,
        id: Optional[UUID] = None,
        question_id: Optional[UUID] = None,
    ) -> None:
        """Initializes a Suggestion with a value, question_name, type, score, agent, id, and question_id.
        A suggestion is a proposed value for a question in a record. Typically a suggestion is created by a model
        and is used to propose a value for a question in a record. The suggestion can be accepted or rejected by a user.
        Args:
            value (Any): The value of the suggestion.
            question_name (str): The name of the question that the suggestion is proposing a value for.
            type (Optional[Literal["model", "human"]], optional): The type of the suggestion. Defaults to None.
            score (Optional[float], optional): The score of the suggestion. Defaults to None.
            agent (Optional[str], optional): The agent that created the suggestion. Defaults to None.
            id (Optional[UUID], optional): The id of the suggestion. Defaults to None.
            question_id (Optional[UUID], optional): The id of the question that the suggestion is proposing a value for. Defaults to None.
        """
        self._model = SuggestionModel(
            value=value,
            question_name=question_name,
            type=type,
            score=score,
            agent=agent,
            id=id,
            question_id=question_id,
        )

    def __repr__(self) -> str:
        return repr(f"{self.__class__.__name__}({self._model})")

    ####################
    # Public Interface #
    ####################

    @property
    def value(self) -> Any:
        return self._model.value

    @property
    def question_name(self) -> Optional[str]:
        return self._model.question_name

    @question_name.setter
    def question_name(self, value: str) -> None:
        self._model.question_name = value

    @property
    def type(self) -> Optional[Literal["model", "human"]]:
        return self._model.type

    @property
    def score(self) -> Optional[float]:
        return self._model.score

    @property
    def agent(self) -> Optional[str]:
        return self._model.agent

    @property
    def question_id(self) -> Optional[UUID]:
        return self._model.question_id

    @classmethod
    def from_model(cls, model: SuggestionModel) -> "Suggestion":
        return cls(**model.model_dump())

    def serialize(self) -> dict[str, Any]:
        model_dict = self._model.model_dump()
        return model_dict
