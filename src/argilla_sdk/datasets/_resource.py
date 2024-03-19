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
from typing import Optional, Literal, Union
from uuid import UUID, uuid4

from argilla_sdk.client import Argilla
from argilla_sdk._models import DatasetModel
from argilla_sdk._resource import Resource
from argilla_sdk.settings import Settings
from argilla_sdk._models import DatasetModel


__all__ = ["Dataset"]


class Dataset(Resource):
    """Class for interacting with Argilla Datasets"""

    def __init__(
        self,
        name: Optional[str] = None,
        status: Literal["draft", "ready"] = "draft",
        workspace_id: Optional[Union[UUID, str]] = None,
        settings: Settings = Settings(),
        client: Optional["Argilla"] = Argilla(),
        id: Optional[Union[UUID, str]] = uuid4(),
        _model: Optional[DatasetModel] = None,
    ) -> None:
        """Initalizes a Dataset with a client and model
        Args:
            name (str): Name of the dataset. Replaced by random UUID if not assigned.
            status ["draft", "ready"]: Status of the dataset
            workspace_id (UUID): Workspace_id of the dataset
            settings (Settings): Settings class to be used to configure the dataset.
            client (Argilla): Instance of Argilla to connect with the server.
            id: (UUID): To predefine dataset_id or to reference existing datasets.
                Random UUID is used if not assigned.
        """
        super().__init__(client=client, api=client._datasets)
        if name is None:
            name = str(id)
            self.log(f"Settings dataset name to unique UUID: {id}")
        if _model is None:
            self._model = DatasetModel(
                name=name,
                status=status,
                workspace_id=self._convert_optional_uuid(uuid=workspace_id),
                id=self._convert_optional_uuid(uuid=id),
            )
        else:
            self._model = _model
        self._sync(model=self._model)
        self.__define_settings(settings=settings)

    def __define_settings(
        self,
        settings: Settings,
    ) -> None:
        """Populate the dataset object with settings"""
        self.guidelines = settings.guidelines
        self.fields = settings.fields
        self.questions = settings.questions
        self.allow_extra_metadata = settings.allow_extra_metadata
