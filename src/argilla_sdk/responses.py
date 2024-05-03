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

from typing import Any, TYPE_CHECKING, List, Dict, Optional
from uuid import UUID

from argilla_sdk._models import UserResponseModel, ResponseStatus
from argilla_sdk._resource import Resource

if TYPE_CHECKING:
    from argilla_sdk import Argilla

__all__ = ["Response", "UserResponse"]


class Response:
    """Class for interacting with Argilla Responses of records. Responses are answers to questions by a user.
    Therefore, a recod question can have multiple responses, one for each user that has answered the question.
    A `Response` is typically created by a user in the UI or consumed from a data source as a label,
    unlike a `Suggestion` which is typically created by a model prediction.

    """

    def __init__(
        self,
        question_name: str,
        value: Any,
        user_id: UUID,
    ) -> None:
        """Initializes a `Response` for a `Record` with a user_id and value"""

        self.question_name = question_name
        self.value = value
        self.user_id = user_id

    def serialize(self) -> dict[str, Any]:
        """Serializes the Response to a dictionary. This is principally used for sending the response to the API, \
            but can be used for data wrangling or manual export.
        
        Returns:
            dict[str, Any]: The serialized response as a dictionary with keys `question_name`, `value`, and `user_id`.
            
        Examples:
        
        ```python
        response = rg.Response("label", "negative", user_id=user.id)
        response.serialize()
        ```
        """
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
    of responses to questions for a given user. UserResponses are typically created by a user in the UI and
    are defined by ingesting a list of responses from a third-party data source.

    In most cases users will interact with the `UserResponse` class through the `Record` class when
    collected from the server or when creating new records.

    Attributes:
        status (ResponseStatus): The status of the UserResponse (draft, submitted, etc.)
        user_id (UUID): The user_id of the UserResponse (the user who answered the questions)
        answers (List[Response]): A list of responses to questions for the user

    """

    _model: UserResponseModel

    def __init__(
        self,
        user_id: UUID,
        answers: List[Response],
        status: ResponseStatus = "draft",
        client: Optional["Argilla"] = None,
    ) -> None:
        """Initializes a UserResponse with a user and a set of question answers"""

        super().__init__(client=client)

        self._model = UserResponseModel(
            values=self.__create_response_values(answers),
            status=status,
            user_id=user_id,
        )

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
    def from_model(cls, model: UserResponseModel) -> "UserResponse":
        """Creates a UserResponse from a ResponseModel"""
        return cls(
            model.user_id,
            answers=cls.__model_as_response_list(model),
            status=model.status,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Returns the UserResponse as a dictionary"""
        return self._model.dict()

    @staticmethod
    def __create_response_values(answers: List[Response]) -> Dict[str, Dict[str, str]]:
        return {answer.question_name: {"value": answer.value} for answer in answers}

    @staticmethod
    def __model_as_response_list(model: UserResponseModel) -> List[Response]:
        """Creates a list of Responses from a UserResponseModel"""
        return [
            Response(question_name=question_name, value=value["value"], user_id=model.user_id)
            for question_name, value in model.values.items()
        ]
