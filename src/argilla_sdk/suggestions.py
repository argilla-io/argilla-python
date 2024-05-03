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
    """Class for interacting with Argilla Suggestions. Suggestions are typically model predictions for records.
    Suggestions are rendered in the user interfaces as 'hints' or 'suggestions' for the user to review and accept or reject.

    Attributes:
        value (str): The value of the suggestion.add()
        question_name (str): The name of the question that the suggestion is for.
        type (str): The type of suggestion, either 'model' or 'human'.
        score (float): The score of the suggestion. For example, the probability of the model prediction.
        agent (str): The agent that created the suggestion. For example, the model name.
        question_id (UUID): The ID of the question that the suggestion is for.

    """

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

    ##############################
    # Properties
    ##############################

    @property
    def value(self) -> Any:
        """The value of the suggestion."""
        return self._model.value

    @property
    def question_name(self) -> Optional[str]:
        """The name of the question that the suggestion is for."""
        return self._model.question_name

    @question_name.setter
    def question_name(self, value: str) -> None:
        self._model.question_name = value

    @property
    def type(self) -> Optional[Literal["model", "human"]]:
        """The type of suggestion, either 'model' or 'human'."""
        return self._model.type

    @property
    def score(self) -> Optional[float]:
        """The score of the suggestion."""
        return self._model.score

    @property
    def agent(self) -> Optional[str]:
        """The agent that created the suggestion."""
        return self._model.agent

    @property
    def question_id(self) -> Optional[UUID]:
        """The ID of the question that the suggestion is for."""
        return self._model.question_id

    @classmethod
    def from_model(cls, model: SuggestionModel) -> "Suggestion":
        return cls(**model.model_dump())
