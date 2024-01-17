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
from typing import Any, ClassVar, Dict, List, Literal, Optional

__all__ = ["LabelOption", "LabelSettings", "MultiLabelSettings"]


@dataclass
class LabelOption:
    value: str
    text: str
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "text": self.text,
            "description": self.description,
        }


@dataclass
class LabelSettings:
    type: ClassVar[Literal["label_selection"]] = "label_selection"
    options: List[LabelOption] = field(default_factory=list)
    visible_options: Optional[int] = None

    @classmethod
    def from_labels(cls, labels: List[str]) -> "LabelSettings":
        """Create a list of LabelOption from a list of labels"""
        return cls(options=[LabelOption(value=label, text=label) for label in labels])

    def __post_init__(self):
        for index, option in enumerate(self.options):
            if isinstance(option, dict):
                self.options[index] = LabelOption(**option)

    def to_dict(self):
        return {
            "type": self.type,
            "options": [option.to_dict() for option in self.options],
            "visible_options": self.visible_options,
        }


@dataclass
class MultiLabelSettings(LabelSettings):
    type: ClassVar[Literal["multi_label_selection"]] = "multi_label_selection"
