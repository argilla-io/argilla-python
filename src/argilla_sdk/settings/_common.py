from typing import Optional, Union


from argilla_sdk._resource import Resource
from argilla_sdk._models import FieldBaseModel, QuestionBaseModel
from argilla_sdk._resource import Resource

__all__ = ["SettingsPropertyBase"]


class SettingsPropertyBase(Resource):
    """Base class for dataset fields or questions in Settings class"""

    _model: Union[FieldBaseModel, QuestionBaseModel]

    @property
    def name(self) -> str:
        return self._model.name

    @property
    def title(self) -> Optional[str]:
        return self._model.title

    @property
    def required(self) -> bool:
        return self._model.required

    @property
    def description(self) -> Optional[str]:
        return self._model.description

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, title={self.title}, description={self.description}, type={self._model.settings.type}, required={self.required}) \n"
