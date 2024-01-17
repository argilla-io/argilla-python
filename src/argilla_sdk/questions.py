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

from typing import List, TYPE_CHECKING

from argilla_sdk import _api
from argilla_sdk._api._questions import QuestionSettings, LabelOption, RankingOption, RatingOption, SettingsType  # noqa
from argilla_sdk._helpers._iterator import GenericIterator  # noqa

if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset

__all__ = [
    "Question",
    "QuestionSettings",
    "DatasetQuestions",
    "RatingOption",
    "LabelOption",
    "RankingOption",
]


class Question(_api.Question):
    def validate(self):
        pass

    @property
    def dataset(self) -> "Dataset":
        from argilla_sdk.datasets import Dataset

        return Dataset.get(self.dataset_id)

    @dataset.setter
    def dataset(self, dataset: "Dataset"):
        self.dataset_id = dataset.id


QuestionsIterator = GenericIterator[Question]


class DatasetQuestions:
    def __init__(self, dataset: "Dataset"):
        self.dataset = dataset

    def list(self) -> List[Question]:
        return Question.list_by_dataset_id(self.dataset.id)

    def add(self, question: Question) -> Question:
        question.dataset_id = self.dataset.id
        return question.create()

    def get_by_name(self, name: str) -> Question:
        return Question.get_by_name(self.dataset.id, name=name)

    def __getitem__(self, key: str) -> Question:
        return self.get_by_name(key)

    def __iter__(self):
        return QuestionsIterator(self.list())
