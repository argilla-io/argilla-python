from typing import Optional

from argilla_sdk._resource import Resource
from argilla_sdk._models import TextFieldModel, FieldSettings


__all__ = ["TextField"]


class FieldBase(Resource):
    """Base class for dataset fields in Settings class"""

    pass


class TextField(FieldBase):
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
            required=required,
            description=description,
            settings=FieldSettings(type="text", use_markdown=use_markdown),
        )

    @property
    def name(self) -> str:
        return self._model.name

    @property
    def title(self) -> str:
        return self._model.title

    @property
    def required(self) -> bool:
        return self._model.required

    @property
    def description(self) -> str:
        return self._model.description

    @property
    def use_markdown(self) -> bool:
        return self._model.settings.use_markdown
