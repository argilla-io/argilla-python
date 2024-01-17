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

from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Literal, Union

__all__ = ["RatingSettings", "RatingOption"]


@dataclass
class RatingOption:
    value: int

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value}


@dataclass
class RatingSettings:
    type: ClassVar[Literal["rating"]] = "rating"
    options: List[Union[dict, RatingOption]] = field(default_factory=list)

    @classmethod
    def from_boundaries(cls, min: int = 1, max: int = 10) -> "RatingSettings":
        return cls(options=[RatingOption(value) for value in range(min, max + 1)])

    def __post_init__(self):
        for index, option in enumerate(self.options):
            if isinstance(option, dict):
                self.options[index] = RatingOption(**option)

    def to_dict(self):
        return {
            "type": self.type,
            "options": [option.to_dict() for option in self.options],
        }
