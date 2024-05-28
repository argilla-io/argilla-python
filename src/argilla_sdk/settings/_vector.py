from typing import Optional, TYPE_CHECKING

from argilla_sdk._api._vectors import VectorsAPI
from argilla_sdk._models import VectorFieldModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla

if TYPE_CHECKING:
    from argilla_sdk import Dataset

__all__ = ["VectorField"]


class VectorField(Resource):
    """Vector field for use in Argilla `Dataset` `Settings`"""

    _model: VectorFieldModel
    _api: VectorsAPI

    def __init__(
        self,
        name: str,
        dimensions: int,
        title: Optional[str] = None,
        _client: Optional["Argilla"] = None,
    ) -> None:
        """Vector field for use in Argilla `Dataset` `Settings`

        Parameters:
            name (str): The name of the field
            dimensions (int): The number of dimensions in the vector
            title (Optional[str], optional): The title of the field. Defaults to None.
        """
        client = _client or Argilla._get_default()
        super().__init__(api=client.api.vectors, client=client)
        self._model = VectorFieldModel(name=name, title=title, dimensions=dimensions)
        self._dataset = None

    @property
    def name(self) -> str:
        return self._model.name

    @name.setter
    def name(self, value: str) -> None:
        self._model.name = value

    @property
    def title(self) -> Optional[str]:
        return self._model.title

    @title.setter
    def title(self, value: Optional[str]) -> None:
        self._model.title = value

    @property
    def dimensions(self) -> int:
        return self._model.dimensions

    @dimensions.setter
    def dimensions(self, value: int) -> None:
        self._model.dimensions = value

    @property
    def dataset(self) -> "Dataset":
        return self._dataset

    @dataset.setter
    def dataset(self, value: "Dataset") -> None:
        self._dataset = value
        self._model.dataset_id = self._dataset.id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, title={self.title}, dimensions={self.dimensions})"

    @classmethod
    def from_model(cls, model: VectorFieldModel) -> "VectorField":
        instance = cls(name=model.name, dimensions=model.dimensions)
        instance._model = model

        return instance

    @classmethod
    def from_dict(cls, data: dict) -> "VectorField":
        model = VectorFieldModel(**data)
        return cls.from_model(model=model)

    def _sync(self, model: "VectorFieldModel") -> None:
        self._model = model