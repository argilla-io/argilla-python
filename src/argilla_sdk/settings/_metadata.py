from typing import Optional, Union

from argilla_sdk._exceptions import MetadataError
from argilla_sdk._models import (
    MetadataPropertyType,
    TermsMetadataPropertySettings,
    FloatMetadataPropertySettings,
    IntegerMetadataPropertySettings,
    MetadataField,
)
from argilla_sdk.settings._common import SettingsPropertyBase


__all__ = [
    "TermsMetadataProperty",
    "FloatMetadataProperty",
    "IntegerMetadataProperty",
    "MetadataType",
]


class MetadataPropertyBase(SettingsPropertyBase):
    _model: MetadataField


class TermsMetadataProperty(MetadataPropertyBase):
    def __init__(self, name: str, options: list[str], title: Optional[str] = None) -> None:
        """Create a metadata field with terms settings.
        Args:
            name (str): The name of the metadata field
            options (list[str]): The list of terms
            title (Optional[str]): The title of the metadata field
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

        self._model = MetadataField(
            name=name,
            type=MetadataPropertyType.terms,
            title=title,
            settings=settings,
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

        self._model = MetadataField(
            name=name,
            type=MetadataPropertyType.float,
            title=title,
            settings=settings,
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

        self._model = MetadataField(
            name=name,
            type=MetadataPropertyType.integer,
            title=title,
            settings=settings,
        )


MetadataType = Union[TermsMetadataProperty, FloatMetadataProperty, IntegerMetadataProperty]


class _MetadataField:
    """Internal utility class for creating metadata fields from metadata models
    returned by the API.
    """

    @classmethod
    def from_model(cls, model: MetadataField) -> MetadataType:
        """Create a metadata field from a metadata model. Switch class based on the metadata type.
        Args:
            model (MetadataField): The metadata model
        Returns:
            MetadataType: The metadata field of a given type.
        """
        metadata_type = model.settings.type
        if metadata_type == MetadataPropertyType.terms:
            return TermsMetadataProperty(
                name=model.name,
                options=model.settings.values,
                title=model.title,
            )
        elif metadata_type == MetadataPropertyType.float:
            return FloatMetadataProperty(
                name=model.name,
                min=model.settings.min,
                max=model.settings.max,
                title=model.title,
            )
        elif metadata_type == MetadataPropertyType.integer:
            return IntegerMetadataProperty(
                name=model.name,
                min=model.settings.min,
                max=model.settings.max,
                title=model.title,
            )
        else:
            raise MetadataError(f"Unknown metadata property type: {metadata_type}")
