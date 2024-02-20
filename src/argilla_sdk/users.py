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
from argilla_sdk._models import UserModel
from argilla_sdk._resource import Resource

__all__ = ["User"]


class User(Resource):
    def __init__(self, **kwargs) -> None:
        self._model = UserModel(**kwargs)
        self.username = self._model.username
        self.first_name = self._model.first_name
        self.role = self._model.role

        self.id = self._model.id
        self.last_name = self._model.last_name
        self.password = self._model.password
        self.inserted_at = self._model.inserted_at
        self.updated_at = self._model.updated_at
