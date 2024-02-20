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
from typing import ClassVar, List, Literal, Optional

__all__ = ["RankingOption", "RankingSettings"]


@dataclass
class RankingOption:
    value: str
    text: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self):
        if self.text is None:
            self.text = self.value

    def to_dict(self):
        return {
            "value": self.value,
            "text": self.text,
            "description": self.description,
        }


@dataclass
class RankingSettings:
    type: ClassVar[Literal["ranking"]] = "ranking"
    options: List[RankingOption] = field(default_factory=list)

    @classmethod
    def from_labels(cls, labels: List[str]):
        return cls(options=[RankingOption(value=label) for label in labels])

    def __post_init__(self):
        for index, option in enumerate(self.options):
            if isinstance(option, dict):
                self.options[index] = RankingOption(**option)

    def to_dict(self):
        return {
            "type": self.type,
            "options": [option.to_dict() for option in self.options],
        }
