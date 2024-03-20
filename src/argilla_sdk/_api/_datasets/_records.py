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

from typing import List, Dict
from uuid import UUID

import httpx
from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceAPI
from argilla_sdk._models import RecordModel

__all__ = ["RecordsAPI"]


class RecordsAPI(ResourceAPI[RecordModel]):
    """Manage datasets via the API"""

    http_client: httpx.Client

    ################
    # CRUD methods #
    ################

    def read(self, record_id: UUID) -> RecordModel:
        response = self.http_client.get(f"/api/v1/records/{record_id}")
        _http.raise_for_status(response=response)
        return self._model_from_json(response_json=response.json())

    def update(self, record: RecordModel) -> RecordModel:
        response = self.http_client.patch(
            url=f"/api/v1/records/{record.id}",
            json=record.model_dump(),
        )
        _http.raise_for_status(response=response)
        return self._model_from_json(response_json=response.json())

    def delete(self, record_id: UUID) -> None:
        response = self.http_client.delete(f"/api/v1/records/{record_id}")
        _http.raise_for_status(response=response)
        self.log(message=f"Deleted record {record_id}")

    ####################
    # Utility methods #
    ####################

    def create_many(self, dataset_id: UUID, records: List[Dict]) -> None:
        response = self.http_client.post(
            url=f"/api/v1/datasets/{dataset_id}/records",
            json={"items": records},
        )
        _http.raise_for_status(response=response)
        self.log(message=f"Created {len(records)} records in dataset {dataset_id}")
        # TODO: Once server returns the records, return them here

    def list(self, dataset_id: UUID, with_suggestions: bool = True, with_responses: bool = True) -> List[RecordModel]:
        include = [
            "suggestions" if with_suggestions else "",
            "responses" if with_responses else "",
        ]
        params = {"include": ",".join(include)}
        response = self.http_client.get(f"/api/v1/datasets/{dataset_id}/records", params=params)
        _http.raise_for_status(response=response)
        json_records = response.json()["items"]
        return self._model_from_jsons(response_jsons=json_records)

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, response_json: Dict) -> RecordModel:
        response_json["inserted_at"] = self._date_from_iso_format(date=response_json["inserted_at"])
        response_json["updated_at"] = self._date_from_iso_format(date=response_json["updated_at"])
        return RecordModel(**response_json)

    def _model_from_jsons(self, response_jsons: List[dict]) -> List[RecordModel]:
        return list(map(self._model_from_json, response_jsons))
