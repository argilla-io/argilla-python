from typing import Optional, Union

from argilla_sdk._exceptions import MetadataError
from argilla_sdk._models import (
    MetadataPropertyType,
    TermsMetadataPropertySettings,
    FloatMetadataPropertySettings,
    IntegerMetadataPropertySettings,
    MetadataFieldModel,
)
from argilla_sdk.settings._common import SettingsPropertyBase


__all__ = [
    "TermsMetadataProperty",
    "FloatMetadataProperty",
    "IntegerMetadataProperty",
    "MetadataType",
]


class MetadataPropertyBase(SettingsPropertyBase):
    _model: MetadataFieldModel


class TermsMetadataProperty(MetadataPropertyBase):
    def __init__(self, name: str, options: list[str], title: Optional[str] = None) -> None:
        """Create a metadata field with terms settings.

        Parameters:
            name (str): The name of the metadata field
            options (list[str]): The list of terms
            title (Optional[str]): The title of the metadata field
        Raises:
            MetadataError: If an error occurs while defining metadata settings
        """

        try:
            settings = TermsMetadataPropertySettings(values=options, type=MetadataPropertyType.terms)
        except ValueError as e:
            raise MetadataError(f"Error defining metadata settings for {name}") from e

        self._model = MetadataFieldModel(
            name=name,
            type=MetadataPropertyType.terms,
            title=title,
            settings=settings,
        )

    @classmethod
    def from_model(cls, model: MetadataFieldModel) -> "TermsMetadataProperty":
        return TermsMetadataProperty(
            name=model.name,
            options=model.settings.values,
            title=model.title,
        )


class FloatMetadataProperty(MetadataPropertyBase):
    def __init__(
        self, name: str, min: Optional[float] = None, max: Optional[float] = None, title: Optional[str] = None
    ) -> None:
        """Create a metadata field with float settings.

        Parameters:
            name (str): The name of the metadata field
            min (Optional[float]): The minimum value
            max (Optional[float]): The maximum value
            title (Optional[str]): The title of the metadata field
        Raises:
            MetadataError: If an error occurs while defining metadata settings


        """
        try:
            settings = FloatMetadataPropertySettings(min=min, max=max, type=MetadataPropertyType.float)
        except ValueError as e:
            raise MetadataError(f"Error defining metadata settings for {name}") from e

        self._model = MetadataFieldModel(
            name=name,
            type=MetadataPropertyType.float,
            title=title,
            settings=settings,
        )

    @classmethod
    def from_model(cls, model: MetadataFieldModel) -> "FloatMetadataProperty":
        return FloatMetadataProperty(
            name=model.name,
            min=model.settings.min,
            max=model.settings.max,
            title=model.title,
        )


class IntegerMetadataProperty(MetadataPropertyBase):
    def __init__(
        self, name: str, min: Optional[int] = None, max: Optional[int] = None, title: Optional[str] = None
    ) -> None:
        """Create a metadata field with integer settings.

        Parameters:
            name (str): The name of the metadata field
            min (Optional[int]): The minimum value
            max (Optional[int]): The maximum value
            title (Optional[str]): The title of the metadata field
        Raises:
            MetadataError: If an error occurs while defining metadata settings
        """

        try:
            settings = IntegerMetadataPropertySettings(min=min, max=max, type=MetadataPropertyType.integer)
        except ValueError as e:
            raise MetadataError(f"Error defining metadata settings for {name}") from e

        self._model = MetadataFieldModel(
            name=name,
            type=MetadataPropertyType.integer,
            title=title,
            settings=settings,
        )

    @classmethod
    def from_model(cls, model: MetadataFieldModel) -> "IntegerMetadataProperty":
        return IntegerMetadataProperty(
            name=model.name,
            min=model.settings.min,
            max=model.settings.max,
            title=model.title,
        )


MetadataType = Union[TermsMetadataProperty, FloatMetadataProperty, IntegerMetadataProperty]


class MetadataField:
    @classmethod
    def from_model(cls, model: MetadataFieldModel) -> MetadataType:
        switch = {
            MetadataPropertyType.terms: TermsMetadataProperty,
            MetadataPropertyType.float: FloatMetadataProperty,
            MetadataPropertyType.integer: IntegerMetadataProperty,
        }
        metadata_type = model.type
        try:
            return switch[metadata_type].from_model(model)
        except KeyError as e:
            raise MetadataError(f"Unknown metadata property type: {metadata_type}") from e
