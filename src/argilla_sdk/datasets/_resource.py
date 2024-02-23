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
from typing import Union, Optional, List, Dict

from argilla_sdk._resource import Resource
from argilla_sdk.settings import Settings
from argilla_sdk.settings.fields import TextField
from argilla_sdk.settings.questions import LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion
from argilla_sdk._models import DatasetModel, RecordModel

__all__ = ["Dataset"]


class Dataset(Resource):
    def __init__(
        self,
        settings: Settings = Settings(),
        guidelines: Union[str, None] = None,
        fields: Optional[list[TextField]] = None,
        questions: Optional[list[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion]]] = None,
        **kwargs,
    ) -> None:
        self._model = DatasetModel(**kwargs)
        self.__define_settings(settings=settings, guidelines=guidelines, fields=fields, questions=questions)
        self.__remote_records_cache = []
        self.__records = []

    @property
    def records(self) -> int:
        return self.__records

    @records.setter
    def records(self, values: List[Union[Dict, RecordModel]]) -> None:
        record_models = [RecordModel(**record) if isinstance(record, dict) else record for record in values]
        self.__records = record_models

    def __define_settings(
        self,
        settings: Settings,
        guidelines: Union[str, None] = None,
        fields: Optional[list[TextField]] = None,
        questions: Optional[list[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion]]] = None,
    ) -> None:
        self.guidelines = guidelines or settings.guidelines
        self.fields = fields or settings.fields
        self.questions = questions or settings.questions

    ###################
    # Update methods  #
    ###################

    def _update(self, **kwargs) -> None:
        super()._update(**kwargs)
        self.__update_remote_records()

    def __update_remote_records(self) -> None:
        local_records_cache = self.__hash_cache_records(normalised_records=self.__records)
        if set(local_records_cache) != set(self.__remote_records_cache):
            records = [record._model.model_dump() for record in self.records]
            self.api._datasets.create_records(dataset_id=self.id, records=records)
            self.__remote_records_cache = local_records_cache

    def __hash_cache_records(self, normalised_records) -> List[int]:
        return [hash(record) for record in normalised_records]
