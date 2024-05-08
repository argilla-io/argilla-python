from typing import Optional, Union

from argilla_sdk._models import FieldModel, FieldSettings, MetadataFieldModel, TextFieldModel, VectorFieldModel
from argilla_sdk.settings._common import SettingsPropertyBase
from argilla_sdk.settings._metadata import MetadataField

__all__ = ["TextField", "FieldType", "VectorField"]


class TextField(SettingsPropertyBase):
    """Text field for use in Argilla `Dataset` `Settings`"""

    _model: TextFieldModel

    def __init__(
        self,
        name: str,
        title: Optional[str] = None,
        use_markdown: Optional[bool] = False,
        required: Optional[bool] = True,
        description: Optional[str] = None,
    ) -> None:
        """Text field for use in Argilla `Dataset` `Settings`
        Parameters:
            name (str): The name of the field
            title (Optional[str], optional): The title of the field. Defaults to None.
            use_markdown (Optional[bool], optional): Whether to use markdown. Defaults to False.
            required (Optional[bool], optional): Whether the field is required. Defaults to True.
            description (Optional[str], optional): The description of the field. Defaults to None.

        """
        self._model = TextFieldModel(
            name=name,
            title=title,
            required=required or True,
            description=description,
            settings=FieldSettings(type="text", use_markdown=use_markdown),
        )

    @property
    def use_markdown(self) -> Optional[bool]:
        return self._model.settings.use_markdown

    @classmethod
    def from_model(cls, model: TextFieldModel) -> "TextField":
        instance = cls(name=model.name)
        instance._model = model

        return instance


class VectorField(SettingsPropertyBase):
    """Vector field for use in Argilla `Dataset` `Settings`"""

    _model: VectorFieldModel

    def __init__(
        self,
        name: str,
        dimensions: int,
        title: Optional[str] = None,
    ) -> None:
        """Vector field for use in Argilla `Dataset` `Settings`

        Parameters:
            name (str): The name of the field
            dimensions (int): The number of dimensions in the vector
            title (Optional[str], optional): The title of the field. Defaults to None.
        """
        self._model = VectorFieldModel(
            name=name,
            title=title,
            dimensions=dimensions,
        )

    @classmethod
    def from_model(cls, model: VectorFieldModel) -> "VectorField":
        instance = cls(name=model.name, dimensions=model.dimensions)
        instance._model = model

        return instance

    @property
    def dimensions(self) -> int:
        return self._model.dimensions

    @property
    def title(self) -> Optional[str]:
        return self._model.title

    @property
    def name(self) -> str:
        return self._model.name


FieldType = Union[TextField, VectorField, MetadataField]


def field_from_model(model: FieldModel) -> FieldType:
    """Create a field instance from a field model"""
    if isinstance(model, TextFieldModel):
        return TextField.from_model(model)
    elif isinstance(model, VectorFieldModel):
        return VectorField.from_model(model)
    elif isinstance(model, MetadataFieldModel):
        return MetadataField.from_model(model)
    else:
        raise ValueError(f"Unsupported field model type: {type(model)}")
