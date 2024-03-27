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

from argilla_sdk._models import ResponseModel, ResponseStatus
from argilla_sdk._resource import Resource

__all__ = ["Response"]


class Response(Resource):
    """Class for interacting with Argilla Responses of records"""

    _model: ResponseModel

    def __init__(
        self,
        question_name: str,
        value: str,
        user_id: str,
        status: ResponseStatus = "draft",
    ) -> None:
        """Initializes a Response with a user_id and value"""
        self._model = ResponseModel(
            values=self.__create_response_values(question_name, value),
            status=status,
            user_id=user_id,
        )

    ####################
    # Public Interface #
    ####################

    @property
    def question_name(self) -> str:
        """Returns the question name of the Response"""
        return list(self._model.values.keys())[0]

    @property
    def value(self) -> str:
        """Returns the value of the Response"""
        return self._model.values[self.question_name]["value"]

    @property
    def user_id(self) -> str:
        """Returns the user_id of the Response"""
        return self._model.user_id

    @classmethod
    def from_model(cls, model: ResponseModel) -> "Response":
        """Creates a Response from a ResponseModel"""
        question_name = list(model.values.keys())[0]
        value = model.values[question_name]["value"]
        user_id = str(model.user_id)
        status = model.status
        return cls(question_name, value, user_id, status)

    #####################
    # Private Interface #
    #####################

    def __create_response_values(self, question_name, value):
        return {question_name: {"value": value}}
