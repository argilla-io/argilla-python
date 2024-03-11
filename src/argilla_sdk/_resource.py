from typing import Any, TYPE_CHECKING

from argilla_sdk._helpers._mixins import LoggingMixin, UUIDMixin

if TYPE_CHECKING:
    from argilla_sdk.client import Argilla
    from argilla_sdk._models import ResourceModel
    from argilla_sdk._api._base import ResourceAPI


class Resource(LoggingMixin, UUIDMixin):
    """Base class for all resources (Dataset, Workspace, User, etc.)"""

    _model: "ResourceModel"
    _client: "Argilla"
    _api: "ResourceAPI"

    def __init__(self, api: "ResourceAPI", client: "Argilla") -> None:
        self._client = client
        self._api = api

    def __repr__(self) -> str:
        return repr(f"{self.__class__.__name__}({self._model})")

    def _sync(self, model: "ResourceModel"):
        """Updates the resource with the ClientAPI that is used to interact with
        Argilla and adds an updated model to the resource.
        Args:
            model (Union[WorkspaceModel, UserModel, DatasetModel]): The updated model
        Returns:
            Self: The updated resource
        """
        self._model = model
        # set all attributes from the model to the resource
        for field in self._model.model_fields:
            setattr(self, field, getattr(self._model, field))
        return self

    ############################
    # CRUD operations
    ############################

    def create(self) -> "Resource":
        response_model = self._api.create(self._model)
        self._sync(response_model)
        return self

    def get(self) -> "Resource":
        response_model = self._api.get(self._model.id)
        self._sync(response_model)
        return self

    def update(self) -> "Resource":
        response_model = self._api.update(self._model)
        self._sync(response_model)
        return self

    def delete(self) -> None:
        self._api.delete(self._model.id)
        self._model = None

    ############################
    # Serialization
    ############################

    def serialize(self) -> dict[str, Any]:
        return self._model.model_dump()

    def serialize_json(self) -> str:
        return self._model.model_dump_json()
