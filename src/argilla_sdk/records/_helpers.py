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

from typing import Any, Dict


def _dict_to_record(record_dict: Dict[str, Any]) -> "Record":
    """Converts a dictionary to a Record object.
    Args:
        record_dict (Dict[str, Any]): The dictionary to convert to a Record object.
    Returns:
        Record: The Record object.
    """
    from argilla_sdk import Suggestion, Response, Record, Vector

    fields = record_dict.get("fields", [])
    metadata = record_dict.get("metadata", {})
    suggestions = record_dict.get("suggestions", [])
    responses = record_dict.get("responses", [])
    vectors = record_dict.get("vectors", {})
    external_id = record_dict.get("id", None)

    suggestions = [Suggestion(question_name=question_name, **value) for question_name, value in suggestions.items()]
    responses = [
        Response(question_name=question_name, **value)
        for question_name, _responses in responses.items()
        for value in _responses
    ]
    vectors = [Vector(name=vector_name, values=values) for vector_name, values in vectors.items()]

    return Record(
        id=external_id,
        fields=fields,
        suggestions=suggestions,
        responses=responses,
        metadata=metadata,
        vectors=vectors,
    )
