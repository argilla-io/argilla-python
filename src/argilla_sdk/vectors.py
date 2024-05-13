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

from typing import Any

from argilla_sdk._models import VectorModel
from argilla_sdk._resource import Resource

__all__ = ["Vector"]


class Vector(Resource):
    _model: VectorModel

    def __init__(
        self,
        name: str,
        values: list[float],
    ) -> None:
        """Initializes a Vector with a name and values that can
        be used to search in the Argilla ui.
        Args:
            name (str): Name of the vector
            values (list[float]): List of float values
        """
        self._model = VectorModel(
            name=name,
            vector_values=values,
        )

    def __repr__(self) -> str:
        return repr(f"{self.__class__.__name__}({self._model})")

    @property
    def name(self) -> str:
        return self._model.name

    @property
    def values(self) -> list[float]:
        return self._model.vector_values

    @classmethod
    def from_model(cls, model: VectorModel) -> "Vector":
        return cls(
            name=model.name,
            values=model.vector_values,
        )

    def serialize(self) -> dict[str, Any]:
        dumped_model = self._model.model_dump()
        name = dumped_model.pop("name")
        values = dumped_model.pop("vector_values")
        return {name: values}
