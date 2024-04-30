from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import Field, field_serializer, field_validator

from argilla_sdk._models._metadata import MetadataModel
from argilla_sdk._models._resource import ResourceModel
from argilla_sdk._models._response import ResponseModel
from argilla_sdk._models._suggestion import SuggestionModel
from argilla_sdk._models._vector import VectorModel


class RecordModel(ResourceModel):
    """Schema for the records of a `Dataset`"""

    fields: Dict[str, Union[str, None]]
    metadata: Optional[Union[List[MetadataModel], Dict[str, Union[str, List[str], float, int]]]] = Field(default_factory=dict)
    vectors: Optional[List[VectorModel]] = Field(default_factory=list)
    responses: Optional[List[ResponseModel]] = Field(default_factory=list)
    suggestions: Optional[Union[Tuple[SuggestionModel], List[SuggestionModel]]] = Field(default_factory=tuple)

    external_id: Optional[Any] = None

    @field_serializer("external_id", when_used="unless-none")
    def serialize_external_id(self, value: str) -> str:
        return str(value)

    @field_serializer("vectors", when_used="unless-none")
    def serialize_vectors(self, value: List[VectorModel]) -> Dict[str, List[float]]:
        dumped_vectors = [vector.model_dump() for vector in value]
        return {vector["name"]: vector["vector_values"] for vector in dumped_vectors}

    @field_serializer("metadata", when_used="unless-none")
    def serialize_metadata(self, value: List[MetadataModel]) -> Dict[str, Any]:
        """Serialize metadata to a dictionary of key-value pairs based on the metadata name and value."""
        return {metadata.name: metadata.value for metadata in value}

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata(cls, metadata: Union[List[MetadataModel],dict]) -> List[MetadataModel]:
        """Ensure metadata is a list of MetadataModel instances when provided as a dict."""
        if not metadata:
            return []
        if isinstance(metadata, dict):
            return [MetadataModel(name=key, value=value) for key, value in metadata.items()]
        return metadata
