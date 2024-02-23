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

from argilla_sdk._resource import Resource
from argilla_sdk._models import RecordModel, ResponseModel, SuggestionModel

__all__ = ["Record"]


class Record(Resource):
    def __init__(
        self,
        fields: Optional[list[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        vectors: Optional[Dict[str, List[float]]] = None,
        responses: Optional[List[ResponseModel]] = None,
        suggestions: Optional[Union[Tuple[SuggestionModel], List[SuggestionModel]]] = None,
        external_id: Optional[str] = None,
    ) -> None:
        self._model = RecordModel(
            fields=fields,
            metadata=metadata,
            vectors=vectors,
            responses=responses,
            suggestions=suggestions,
            external_id=external_id,
        )
