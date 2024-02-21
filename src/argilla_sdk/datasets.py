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

from argilla_sdk._resource import Resource
from argilla_sdk._models import DatasetModel

__all__ = ["Dataset"]


class Dataset(Resource):
    def __init__(self, **kwargs) -> None:
        self._model = DatasetModel(**kwargs)
        self.name = self._model.name
        self.id = self._model.id
        self.updated_at = self._model.updated_at
        self.workspace_id = self._model.workspace_id
        self.status = self._model.status
        self.guidelines = self._model.guidelines
        self.allow_extra_metadata = self._model.allow_extra_metadata
