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

    @property
    def visible_for_annotators(self) -> Optional[bool]:
        return self._model.visible_for_annotators

    @visible_for_annotators.setter
    def visible_for_annotators(self, value: Optional[bool]) -> None:
        self._model.visible_for_annotators = value


class TermsMetadataProperty(MetadataPropertyBase):
    def __init__(
        self, name: str, options: list[str], title: Optional[str] = None, visible_for_annotators: Optional[bool] = True
    ) -> None:
        """Create a metadata field with terms settings.
        Args:
            name (str): The name of the metadata field
            options (list[str]): The list of terms
            title (Optional[str]): The title of the metadata field
            visible_for_annotators (Optional[bool]): Whether the metadata field is visible for annotators
        Raises:
            MetadataError: If an error occurs while defining metadata settings

        Example:
        ```python
        import argilla_sdk as rg
        metadata_field = rg.TermsMetadataProperty(
            name="color",
            options=["red", "blue", "green"],
            title="Color",
        )
        ```
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
            visible_for_annotators=visible_for_annotators,
        )

    @property
    def options(self) -> list[str]:
        return self._model.settings.values

    @options.setter
    def options(self, value: list[str]) -> None:
        self._model.settings.values = value

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
        Args:
            name (str): The name of the metadata field
            min (Optional[float]): The minimum value
            max (Optional[float]): The maximum value
            title (Optional[str]): The title of the metadata field
        Raises:
            MetadataError: If an error occurs while defining metadata settings

        Example:
        ```python
        import argilla_sdk as rg
        metadata_field = rg.FloatMetadataProperty(
            name="price",
            min=0.0,
            max=100.0,
            title="Price",
        )
        ```
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
        Args:
            name (str): The name of the metadata field
            min (Optional[int]): The minimum value
            max (Optional[int]): The maximum value
            title (Optional[str]): The title of the metadata field
        Raises:
            MetadataError: If an error occurs while defining metadata settings
        Example:
        ```python
        import argilla_sdk as rg
        metadata_field = rg.IntegerMetadataProperty(
            name="quantity",
            min=0,
            max=100,
            title="Quantity",
        )
        ```
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
    """Internal utility class for creating metadata fields from metadata models
    returned by the API.
    """

    @classmethod
    def from_model(cls, model: MetadataFieldModel) -> MetadataType:
        """Create a metadata field from a metadata model. Switch class based on the metadata type.
        Args:
            model (MetadataField): The metadata model
        Returns:
            MetadataType: The metadata field of a given type.
        """
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
