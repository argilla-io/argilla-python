#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from enum import Enum
from typing import List, Literal, Optional, Union, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer, field_validator, model_validator


class MetadataPropertyType(str, Enum):
    terms = "terms"
    integer = "integer"
    float = "float"


class BaseMetadataPropertySettings(BaseModel):
    type: MetadataPropertyType


class TermsMetadataPropertySettings(BaseMetadataPropertySettings):
    type: Literal[MetadataPropertyType.terms]
    values: Optional[List[str]] = None

    @field_validator("values")
    @classmethod
    def __validate_values(cls, values):
        if values is None:
            raise ValueError("Values must be provided for a terms metadata field.")
        elif not isinstance(values, list):
            raise ValueError(f"Values must be a list, got {type(values)}")
        elif not all(isinstance(value, str) for value in values):
            raise ValueError("All values must be strings.")
        return values


class NumericMetadataPropertySettings(BaseMetadataPropertySettings):
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None

    @model_validator(mode="before")
    @classmethod
    def __validate_min_max(cls, values):
        min_value = values.get("min")
        max_value = values.get("max")

        if min_value is not None and max_value is not None:
            if min_value >= max_value:
                raise ValueError("min must be less than max.")
        return values


class IntegerMetadataPropertySettings(NumericMetadataPropertySettings):
    type: Literal[MetadataPropertyType.integer]

    @model_validator(mode="before")
    @classmethod
    def __validate_min_max(cls, values):
        min_value = values.get("min")
        max_value = values.get("max")

        if not all(isinstance(value, int) for value in [min_value, max_value]):
            raise ValueError("min and max must be integers.")
        return values


class FloatMetadataPropertySettings(NumericMetadataPropertySettings):
    type: Literal[MetadataPropertyType.float]


MetadataPropertySettings = Annotated[
    Union[
        TermsMetadataPropertySettings,
        IntegerMetadataPropertySettings,
        FloatMetadataPropertySettings,
    ],
    Field(..., discriminator="type"),
]


class MetadataField(BaseModel):
    """The schema definition of a metadata field in an Argilla dataset."""

    id: Optional[UUID] = None
    name: str
    settings: MetadataPropertySettings

    type: Optional[MetadataPropertyType] = None
    title: Optional[str] = None
    visible_for_annotators: Optional[bool] = True

    @field_validator("name")
    @classmethod
    def __name_lower(cls, name):
        formatted_name = name.lower().replace(" ", "_")
        return formatted_name

    @field_validator("title")
    @classmethod
    def __title_default(cls, title, values):
        validated_title = title or values.data["name"]
        return validated_title

    @field_serializer("id", when_used="unless-none")
    def serialize_id(self, value: UUID) -> str:
        return str(value)

    @field_validator("type", mode="plain")
    def __validate_type(cls, type, values):
        if type is None:
            return values.data["settings"].type
        return type