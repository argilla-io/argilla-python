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

from typing import Optional, Literal, Union, TYPE_CHECKING
from uuid import UUID, uuid4

from argilla_sdk._api import DatasetsAPI
from argilla_sdk._exceptions import ArgillaAPIError
from argilla_sdk._models import DatasetModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla
from argilla_sdk.records import DatasetRecords
from argilla_sdk.settings import Settings

__all__ = ["Dataset"]

if TYPE_CHECKING:
    from argilla_sdk import Workspace


class Dataset(Resource):
    """Class for interacting with Argilla Datasets

    Attributes:
        records (DatasetRecords): The records object
        is_published (bool): True if the dataset is published, False otherwise
        settings (Settings): The settings object
        fields (list): The fields of the dataset
        questions (list): The questions of the dataset
        guidelines (str): The guidelines of the dataset
        allow_extra_metadata (bool): True if extra metadata is allowed, False otherwise
        schema: The schema of the dataset

    """

    name: str
    id: Optional[UUID]
    status: Literal["draft", "ready"]

    _api: "DatasetsAPI"
    _model: "DatasetModel"

    def __init__(
        self,
        name: Optional[str] = None,
        status: Literal["draft", "ready"] = "draft",
        workspace_id: Optional[Union[UUID, str]] = None,
        workspace: Optional["Workspace"] = None,
        settings: Optional[Settings] = None,
        client: Optional["Argilla"] = Argilla(),
        id: Optional[Union[UUID, str]] = uuid4(),
        _model: Optional[DatasetModel] = None,
    ) -> None:
        """Initalizes a new Argilla Dataset object with the given parameters.

        Parameters:
            name (str): The name of the dataset
            status (str): The status of the dataset
            workspace_id (str): The id of the workspace
            workspace (Workspace): The workspace object
            settings (Settings): The settings object
            client (Argilla): The client object
            id (str): The id of the dataset
            _model (DatasetModel): The model object

        Examples:

        To create a new dataset, use the following code:

        ```python
        dataset = rg.Dataset(
            name="my_dataset",
            settings=rg.Settings(
                fields=[
                    rg.TextField(name="text"),
                ],
                questions=[
                    rg.TextQuestion(name="response"),
                ],
            ),
        )
        dataset.publish()
        ```

        To retrieve an existing dataset, use `client.datasets("my_dataset")` instead.

        ```python
        dataset = client.datasets("my_dataset")
        ```

        To connect to an existing workspace refer to the workspace by id or object. For example:

        ```python
        # Get an existing workspace
        workspace = client.workspaces("my_workspace")
        dataset = rg.Dataset(name="my_dataset", workspace=workspace)

        # Use the workspace id
        dataset = rg.Dataset(name="my_dataset", workspace_id="workspace_id")

        # Use the first workspace
        dataset = rg.Dataset(name="my_dataset")

        ```

        """
        super().__init__(client=client, api=client.api.datasets)
        if name is None:
            name = str(id)
            self.log(f"Settings dataset name to unique UUID: {id}")
        self.workspace_id = self.__configure_workspace_for_dataset(workspace_id=workspace_id, workspace=workspace)
        _model = _model or DatasetModel(
            name=name,
            status=status,
            workspace_id=self._convert_optional_uuid(uuid=self.workspace_id),
            id=self._convert_optional_uuid(uuid=id),
        )
        self._model = _model
        self._settings = self.__configure_settings_for_dataset(settings=settings)
        self.__records = DatasetRecords(client=self._client, dataset=self)
        self._sync(model=self._model)

    #####################
    #  Properties       #
    #####################

    @property
    def records(self) -> "DatasetRecords":
        return self.__records

    @property
    def is_published(self) -> bool:
        return self._model.status == "ready"

    @property
    def settings(self) -> Settings:
        if self.is_published and self._settings.is_outdated:
            self._settings.get()
        return self._settings

    @settings.setter
    def settings(self, value: Settings) -> None:
        self._settings = self.__configure_settings_for_dataset(settings=value)

    @property
    def fields(self) -> list:
        return self._settings.fields

    @property
    def questions(self) -> list:
        return self._settings.questions

    @property
    def guidelines(self) -> str:
        return self._settings.guidelines

    @guidelines.setter
    def guidelines(self, value: str) -> None:
        self._settings.guidelines = value

    @property
    def allow_extra_metadata(self) -> bool:
        return self._settings.allow_extra_metadata

    @allow_extra_metadata.setter
    def allow_extra_metadata(self, value: bool) -> None:
        self._settings.allow_extra_metadata = value

    @property
    def schema(self):
        return self._settings.schema

    #####################
    #  Core methods     #
    #####################

    def exists(self) -> bool:
        """Checks if the dataset exists on the server
        Returns:
            bool: True if the dataset exists, False otherwise
        Examples:
        ```python
        dataset = rg.Dataset(name="my_dataset")
        assert dataset.exists() == False
        dataset.create()
        assert dataset.exists() == True
        ```
        """
        return self._api.exists(self.id)

    def publish(self) -> None:
        """Publishes the dataset on the server with the `Settings` conffiguration
        Returns:
            None
        Examples:
        ```python
        dataset = rg.Dataset(name="my_dataset")
        dataset.settings = rg.Settings(...)
        dataset.publish()
        ```


        """
        self._configure(settings=self._settings, publish=True)

    #####################
    #  CRUD operations  #
    #####################

    def create(self) -> "Dataset":
        """Creates a new dataset on the server
        Returns:
            Dataset: The created dataset object
        Examples:
        ```python
        dataset = rg.Dataset(name="my_dataset")
        dataset.create()
        ```
        """
        return super().create()

    def get(self) -> "Dataset":
        """Retrieves the dataset from the server
        Returns:
            Dataset: The retrieved dataset object
        Examples:
        ```python
        dataset = rg.Dataset(name="my_dataset")
        dataset.create()
        # do something to the dataset on the server
        dataset.get() # a dataset object with the latest changes
        ```
        """
        return super().get()

    def update(self) -> "Dataset":
        """Updates the dataset on the server
        Returns:
            Dataset: The updated dataset object
        Examples:
        ```python
        dataset = rg.Dataset(name="my_dataset")
        dataset.create()
        # do something to the dataset configuration locally
        dataset.update()
        ```
        """
        return super().update()

    def delete(self) -> None:
        """Deletes the dataset from the server
        Examples:
        ```python
        dataset = rg.Dataset(name="my_dataset")
        dataset.create()
        dataset.delete()
        ```
        """
        return super().delete()

    #####################
    #  Utility methods  #
    #####################

    # we leave this method as private for now and we use the `ds.publish` one
    def _configure(self, settings: Settings, publish: bool = False) -> "Dataset":
        if not self.exists():
            self.__create()

        self._settings = self.__configure_settings_for_dataset(settings=settings)
        self._settings.create()

        if publish:
            self.__publish()

        return self.get()  # type: ignore

    def __configure_settings_for_dataset(
        self,
        settings: Optional[Settings] = None,
    ) -> Settings:
        settings = settings or Settings()
        settings.dataset = self
        return settings

    def __configure_workspace_for_dataset(
        self, workspace_id: Optional[Union[UUID, str]], workspace: Optional["Workspace"]
    ) -> UUID:
        if workspace_id is not None or workspace is not None:
            workspace_id = workspace_id or workspace.id
            try:
                workspace = self._client.api.workspaces.get(workspace_id=workspace_id)  # type: ignore
            except ArgillaAPIError as e:
                raise ValueError(f"Workspace with id {workspace_id} not found") from e
        else:
            self.log("Setting workspace to first workspace on server")
            workspace = self._client.workspaces[0]
        self.log(f"Using workspace: {workspace.name} id: {workspace.id}")
        return workspace.id

    def __create(self) -> None:
        response_model = self._api.create(self._model)
        self._sync(response_model)

    def __publish(self) -> None:
        if not self.is_published:
            response_model = self._api.publish(dataset_id=self._model.id)
            self._sync(response_model)
