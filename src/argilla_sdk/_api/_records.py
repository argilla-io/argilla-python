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

from typing import List
from uuid import UUID

import httpx
from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceAPI
from argilla_sdk._models import RecordModel

__all__ = ["RecordsAPI"]


class RecordsAPI(ResourceAPI):
    """Manage datasets via the API"""

    http_client: httpx.Client

    ################
    # CRUD methods #
    ################

    def create(self, record: "RecordModel") -> "RecordModel":
        json_body = record.model_dump()
        response = self.http_client.post(
            url="/api/v1/records",
            json=json_body,
        )
        _http.raise_for_status(response=response)
        record = self._model_from_json(json_dataset=response.json())
        return record

    def update(self, record: "RecordModel") -> "RecordModel":
        json_body = record.model_dump()
        record_id = json_body["id"]  # type: ignore
        response = self.http_client.patch(f"/api/v1/records/{record_id}", json=json_body)
        _http.raise_for_status(response=response)
        record = self._model_from_json(json_dataset=response.json())
        return record

    def get(self, record_id: UUID) -> "RecordModel":
        response = self.http_client.get(url=f"/api/v1/records/{record_id}")
        _http.raise_for_status(response=response)
        json_record = response.json()
        record = self._model_from_json(json_dataset=json_record)
        return record

    def delete(self, record_id: UUID) -> None:
        response = self.http_client.delete(f"/api/v1/records/{record_id}")
        _http.raise_for_status(response=response)

    ####################
    # Utility methods #
    ####################

    def create_response(self, record: "RecordModel") -> httpx.Response:
        json_body = record.model_dump()
        response = self.http_client.post(
            url=f"/api/v1/records/{record.id}/responses",
            json=json_body,
        )
        _http.raise_for_status(response=response)
        return response
    
    def get_suggestions(self, record_id: UUID) -> List[str]:
        response = self.http_client.get(f"/api/v1/records/{record_id}/suggestions")
        _http.raise_for_status(response=response)
        return response.json()
    
    def create_or_update_suggestions(self, record_id: UUID, suggestions: List[str]) -> List[str]:
        response = self.http_client.post(f"/api/v1/records/{record_id}/suggestions", json=suggestions)
        _http.raise_for_status(response=response)
        return response.json()
    
    def delete_suggestions(self, record_id: UUID) -> None:
        response = self.http_client.delete(f"/api/v1/records/{record_id}/suggestions")
        _http.raise_for_status(response=response)


    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_dataset: dict) -> "RecordModel":
        json_dataset["inserted_at"] = self._date_from_iso_format(date=json_dataset["inserted_at"])
        json_dataset["updated_at"] = self._date_from_iso_format(date=json_dataset["updated_at"])
        return RecordModel(**json_dataset)

    def _model_from_jsons(self, json_datasets: List[dict]) -> List["RecordModel"]:
        return list(map(self._model_from_json, json_datasets))
