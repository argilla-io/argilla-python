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

from argilla_sdk._models import ResponseModel

__all__ = ["Response"]


class Response:
    def __init__(self, question_name, value, status, user_id) -> None:
        self._model = ResponseModel(
            values=self.__create_response_values(question_name, value),
            status=status,
            user_id=user_id,
        )

    def __create_response_values(self, question_name, value):
        return {question_name: {"value": value}}
