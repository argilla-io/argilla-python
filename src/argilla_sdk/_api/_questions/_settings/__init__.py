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

from typing import Union

from argilla_sdk._api._questions._settings._labels import (
    LabelOption,
    LabelSettings,
    MultiLabelSettings,
)
from argilla_sdk._api._questions._settings._ranking import RankingOption, RankingSettings
from argilla_sdk._api._questions._settings._rating import RatingOption, RatingSettings
from argilla_sdk._api._questions._settings._text import TextSettings

__all__ = [
    "SettingsType",
    "QuestionSettings",
    "RatingOption",
    "LabelOption",
    "RankingOption",
]


QuestionSettings = Union[
    RatingSettings,
    LabelSettings,
    MultiLabelSettings,
    RankingSettings,
    TextSettings,
]  # noqa


class SettingsType:
    _MAP_TYPE_TO_CLASS = {question_class.type: question_class for question_class in QuestionSettings.__args__}  # noqa

    Text = TextSettings
    Rating = RatingSettings
    Label = LabelSettings
    MultiLabel = MultiLabelSettings
    Ranking = RankingSettings

    @classmethod
    def from_dict(cls, data: dict) -> QuestionSettings:
        data_copy = data.copy()
        settings_class = cls._MAP_TYPE_TO_CLASS[data_copy.pop("type")]

        return settings_class(**data_copy)
