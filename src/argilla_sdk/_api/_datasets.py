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

from typing import List, Optional
from uuid import UUID

import httpx
from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceAPI
from argilla_sdk._models._dataset import DatasetModel

__all__ = ["DatasetsAPI"]


class DatasetsAPI(ResourceAPI):
    """Manage datasets via the API"""

    http_client: httpx.Client

    ################
    # CRUD methods #
    ################

    def create(self, dataset: "DatasetModel") -> "DatasetModel":
        json_body = dataset.model_dump()
        response = self.http_client.post(
            url="/api/v1/datasets",
            json=json_body,
        )
        _http.raise_for_status(response=response)
        dataset = self._model_from_json(json_dataset=response.json())
        self.log(message=f"Created dataset {dataset.name}")
        return dataset

    def update(self, dataset: "DatasetModel") -> "DatasetModel":
        json_body = dataset.model_dump()
        dataset_id = json_body["id"]  # type: ignore
        response = self.http_client.patch(f"/api/v1/datasets/{dataset_id}", json=json_body)
        _http.raise_for_status(response=response)
        dataset = self._model_from_json(json_dataset=response.json())
        self.log(message=f"Updated dataset {dataset.url}")
        return dataset

    def get(self, dataset_id: UUID) -> "DatasetModel":
        response = self.http_client.get(url=f"/api/v1/datasets/{dataset_id}")
        _http.raise_for_status(response=response)
        json_dataset = response.json()
        dataset = self._model_from_json(json_dataset=json_dataset)
        self.log(message=f"Got dataset {dataset.url}")
        return dataset

    def delete(self, dataset_id: UUID) -> None:
        response = self.http_client.delete(f"/api/v1/datasets/{dataset_id}")
        _http.raise_for_status(response=response)
        self.log(message=f"Deleted dataset {dataset_id}")

    ####################
    # Utility methods #
    ####################

    def publish(self, dataset_id: UUID) -> "DatasetModel":
        response = self.http_client.put(url=f"/api/v1/datasets/{dataset_id}/publish")
        _http.raise_for_status(response=response)
        self.log(message=f"Published dataset {dataset_id}")
        return self._model_from_json(response.json())

    def list(self, workspace_id: Optional[UUID] = None) -> List["DatasetModel"]:
        response = self.http_client.get("/api/v1/me/datasets")
        _http.raise_for_status(response=response)
        json_datasets = response.json()["items"]
        datasets = self._model_from_jsons(json_datasets=json_datasets)
        if workspace_id:
            datasets = [dataset for dataset in datasets if dataset.workspace_id == workspace_id]
        self.log(message=f"Listed {len(datasets)} datasets")
        return datasets

    def get_by_name_and_workspace_id(self, name: str, workspace_id: UUID) -> Optional["DatasetModel"]:
        datasets = self.list(workspace_id=workspace_id)
        for dataset in datasets:
            if dataset.name == name:
                self.log(message=f"Got dataset {dataset.name}")
                return dataset

    def create_records(self, dataset_id: UUID, records: List[dict]) -> None:
        response = self.http_client.post(
            url=f"/api/v1/datasets/{dataset_id}/records",
            json=records,
        )
        _http.raise_for_status(response=response)
        self.log(message=f"Created {len(records)} records in dataset {dataset_id}")

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_dataset: dict) -> "DatasetModel":
        json_dataset["inserted_at"] = self._date_from_iso_format(date=json_dataset["inserted_at"])
        json_dataset["updated_at"] = self._date_from_iso_format(date=json_dataset["updated_at"])
        return DatasetModel(**json_dataset)

    def _model_from_jsons(self, json_datasets: List[dict]) -> List["DatasetModel"]:
        return list(map(self._model_from_json, json_datasets))
