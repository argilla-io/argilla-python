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

from typing import Any, TYPE_CHECKING, List, Dict, Optional, Iterable
from uuid import UUID

from argilla_sdk._models import UserResponseModel, ResponseStatus
from argilla_sdk._resource import Resource
from argilla_sdk.settings import RankingQuestion

if TYPE_CHECKING:
    from argilla_sdk import Argilla, Dataset, Record

__all__ = ["Response", "UserResponse"]


def ranking_from_model_value(value: List[Dict[str, Any]]) -> List[str]:
    return [v["value"] for v in value]


def ranking_to_model_value(value: List[str]) -> List[Dict[str, str]]:
    return [{"value": v} for v in value]


class Response:
    """Class for interacting with Argilla Responses of records"""

    def __init__(
        self,
        question_name: str,
        value: Any,
        user_id: UUID,
        _record: Optional["Record"] = None,
    ) -> None:
        """Initializes a Response with a user_id and value"""

        if question_name is None:
            raise ValueError("question_name is required")
        if value is None:
            raise ValueError("value is required")
        if user_id is None:
            raise ValueError("user_id is required")

        self.record = _record
        self.question_name = question_name
        self.value = value
        self.user_id = user_id

    def serialize(self) -> dict[str, Any]:
        """Serializes the Response to a dictionary"""
        return {
            "question_name": self.question_name,
            "value": self.value,
            "user_id": self.user_id,
        }

    #####################
    # Private Interface #
    #####################


class UserResponse(Resource):
    """
    Class for interacting with Argilla User Responses of records.  The UserResponse class is a collection
    of responses to questions for a given user.

    """

    _model: UserResponseModel

    def __init__(
        self,
        user_id: UUID,
        answers: List[Response],
        status: ResponseStatus = "draft",
        client: Optional["Argilla"] = None,
        _record: Optional["Record"] = None,
    ) -> None:
        """Initializes a UserResponse with a user and a set of question answers"""

        super().__init__(client=client)

        self._record = _record
        self._model = UserResponseModel(
            values=self.__responses_as_model_values(answers),
            status=status,
            user_id=user_id,
        )

    def __iter__(self) -> Iterable[Response]:
        return iter(self.answers)

    @property
    def status(self) -> ResponseStatus:
        """Returns the status of the UserResponse"""
        return self._model.status

    @status.setter
    def status(self, status: ResponseStatus) -> None:
        """Sets the status of the UserResponse"""
        self._model.status = status

    @property
    def user_id(self) -> UUID:
        """Returns the user_id of the UserResponse"""
        return self._model.user_id

    @user_id.setter
    def user_id(self, user_id: UUID) -> None:
        """Sets the user_id of the UserResponse"""
        self._model.user_id = user_id

    @property
    def answers(self) -> List[Response]:
        """Returns the list of responses"""
        return self.__model_as_response_list(self._model)

    @classmethod
    def from_model(cls, model: UserResponseModel, dataset: "Dataset") -> "UserResponse":
        """Creates a UserResponse from a ResponseModel"""
        answers = cls.__model_as_response_list(model)

        for answer in answers:
            question = dataset.settings.question_by_name(answer.question_name)
            if isinstance(question, RankingQuestion):
                answer.value = ranking_from_model_value(answer.value)  # type: ignore

        return cls(user_id=model.user_id, answers=answers, status=model.status)

    def api_model(self):
        """Returns the model that is used to interact with the API"""

        values = self.__responses_as_model_values(self.answers)
        for question_name, value in values.items():
            question = self._record.dataset.settings.question_by_name(question_name)
            if isinstance(question, RankingQuestion):
                value["value"] = ranking_to_model_value(value["value"])

        return UserResponseModel(values=values, status=self._model.status, user_id=self._model.user_id)

    def to_dict(self) -> Dict[str, Any]:
        """Returns the UserResponse as a dictionary"""
        return self._model.dict()

    @staticmethod
    def __responses_as_model_values(answers: List[Response]) -> Dict[str, Dict[str, Any]]:
        """Creates a dictionary of response values from a list of Responses"""
        return {answer.question_name: {"value": answer.value} for answer in answers}

    @staticmethod
    def __model_as_response_list(model: UserResponseModel) -> List[Response]:
        """Creates a list of Responses from a UserResponseModel"""
        return [
            Response(question_name=question_name, value=value["value"], user_id=model.user_id)
            for question_name, value in model.values.items()
        ]
