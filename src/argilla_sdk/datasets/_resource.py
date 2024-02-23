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
from argilla_sdk.datasets._record import Record

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
        self.__remote_records_cache = {}
        self.__records = {}

    @property
    def records(self) -> int:
        return list(self.__records.values())

    @records.setter
    def records(self, values: List[Union[Dict, RecordModel]]) -> None:
        record_models = []
        for record in values:
            if isinstance(record, dict):
                record_models.append(RecordModel(**record))
            elif isinstance(record, Record):
                record_models.append(record._model)
            elif isinstance(record, RecordModel):
                record_models.append(record)
            else:
                raise ValueError(f"Invalid record type: {type(record)}")
        self.__records = {hash(record): record for record in record_models}

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

    def _sync(self, **kwargs) -> None:
        super()._sync(**kwargs)
        self.__update_remote_records()
        return self

    def __update_remote_records(self) -> None:
        local_records_cache = self.__hash_cache_records(normalised_records=self.__records.values())
        changed_records = {k: v for k, v in local_records_cache.items() if k not in self.__remote_records_cache}
        if changed_records:
            records = [record.model_dump() for record in changed_records.values()]
            self.api._datasets.create_records(dataset_id=self._model.id, records=records)
            self.__remote_records_cache.update(changed_records)

    def __hash_cache_records(self, normalised_records) -> Dict[int, RecordModel]:
        return {hash(record): record for record in normalised_records}
