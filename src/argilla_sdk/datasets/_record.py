# Copyright 2024-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Union, Optional, List, Dict, Tuple, Any
from uuid import uuid4

from argilla_sdk._resource import Resource
from argilla_sdk._models import RecordModel, ResponseModel, SuggestionModel
from argilla_sdk.responses import Response
from argilla_sdk.suggestions import Suggestion

__all__ = ["Record"]


class Record(Resource):
    def __init__(
        self,
        fields: Dict[str, Union[str, None]],
        metadata: Optional[Dict[str, Any]] = None,
        vectors: Optional[Dict[str, List[float]]] = None,
        responses: Optional[List[Response]] = None,
        suggestions: Optional[Union[Tuple[SuggestionModel], List[SuggestionModel]]] = None,
        external_id: Optional[str] = None,
        id: Optional[str] = None,
    ) -> None:
        self._model = RecordModel(
            fields=fields,
            metadata=metadata,
            vectors=vectors,
            external_id=external_id or uuid4(),
            id=id or uuid4(),
        )
        self.__responses = RecordResponses(responses=responses)
        self.__suggestions = RecordSuggestions(suggestions=suggestions)
        self._model.responses = self.__responses.models
        self._model.suggestions = self.__suggestions.models

    def serialize(self) -> RecordModel:
        serialized_model = self._model.model_dump()
        serialized_suggestions = [suggestion.model_dump() for suggestion in self.__suggestions.models]
        serialized_responses = [response.model_dump() for response in self.__responses.models]
        serialized_model["responses"] = serialized_responses
        serialized_model["suggestions"] = serialized_suggestions
        return serialized_model


class RecordResponses:
    def __init__(self, responses: List[Response]) -> None:
        self.__responses = responses or []

    @property
    def models(self) -> List[ResponseModel]:
        return [response._model for response in self.__responses]


class RecordSuggestions:
    def __init__(self, suggestions: List[Suggestion]) -> None:
        self.__suggestions = suggestions or []

    @property
    def models(self) -> List[SuggestionModel]:
        return [suggestion._model for suggestion in self.__suggestions]
