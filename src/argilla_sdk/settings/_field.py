from typing import Optional

from argilla_sdk._models import TextFieldModel, FieldSettings, VectorFieldModel
from argilla_sdk.settings._common import SettingsPropertyBase

__all__ = ["TextField", "FieldType", "VectorField"]


class TextField(SettingsPropertyBase):
    _model: TextFieldModel

    def __init__(
        self,
        name: str,
        title: Optional[str] = None,
        use_markdown: Optional[bool] = False,
        required: Optional[bool] = True,
        description: Optional[str] = None,
    ) -> None:
        """Text field for use in Argilla `Dataset` `Settings`"""
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


class VectorField(SettingsPropertyBase):
    _model: VectorFieldModel

    def __init__(
        self,
        name: str,
        dimensions: int,
        title: Optional[str] = None,
    ) -> None:
        """Vector field for use in Argilla `Dataset` `Settings`"""
        self._model = VectorFieldModel(
            name=name,
            title=title,
            settings=FieldSettings(type="vector"),
            dimensions=dimensions,
        )

    @property
    def dimensions(self) -> int:
        return self._model.dimensions

    @property
    def title(self) -> Optional[str]:
        return self._model.title

    @property
    def name(self) -> str:
        return self._model.name


FieldType = TextField
