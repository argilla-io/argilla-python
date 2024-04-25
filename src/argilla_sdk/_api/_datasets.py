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

from typing import List, Optional, Dict
from uuid import UUID

import httpx
from argilla_sdk._api._base import ResourceAPI
from argilla_sdk._exceptions._api import api_error_handler
from argilla_sdk._models import DatasetModel

__all__ = ["DatasetsAPI"]


class DatasetsAPI(ResourceAPI[DatasetModel]):
    """Manage datasets via the API"""

    http_client: httpx.Client
    url_stub = "/api/v1/datasets"

    ################
    # CRUD methods #
    ################

    @api_error_handler
    def create(self, dataset: "DatasetModel") -> "DatasetModel":
        json_body = dataset.model_dump()
        response = (
            self.http_client.post(
                url=self.url_stub,
                json=json_body,
            )
            .raise_for_status()
            .json()
        )
        dataset = self._model_from_json(json_dataset=response)
        self.log(message=f"Created dataset {dataset.name}")
        return dataset

    @api_error_handler
    def update(self, dataset: "DatasetModel") -> "DatasetModel":
        json_body = dataset.model_dump()
        dataset_id = json_body["id"]  # type: ignore
        response = self.http_client.patch(f"{self.url_stub}/{dataset_id}", json=json_body).raise_for_status().json()
        dataset = self._model_from_json(json_dataset=response)
        self.log(message=f"Updated dataset {dataset.url}")
        return dataset

    @api_error_handler
    def get(self, dataset_id: UUID) -> "DatasetModel":
        response = self.http_client.get(url=f"{self.url_stub}/{dataset_id}").raise_for_status().json()
        dataset = self._model_from_json(json_dataset=response)
        self.log(message=f"Got dataset {dataset.url}")
        return dataset

    @api_error_handler
    def delete(self, dataset_id: UUID) -> None:
        self.http_client.delete(f"{self.url_stub}/{dataset_id}").raise_for_status().json()
        self.log(message=f"Deleted dataset {dataset_id}")

    @api_error_handler
    def exists(self, dataset_id: UUID) -> bool:
        response = self.http_client.get(f"{self.url_stub}/{dataset_id}").raise_for_status()
        return response.status_code == 200

    ####################
    # Utility methods #
    ####################

    @api_error_handler
    def publish(self, dataset_id: UUID) -> "DatasetModel":
        response = self.http_client.put(url=f"{self.url_stub}/{dataset_id}/publish").raise_for_status().json()
        self.log(message=f"Published dataset {dataset_id}")
        return self._model_from_json(response)

    @api_error_handler
    def list(self, workspace_id: Optional[UUID] = None) -> List["DatasetModel"]:
        response = self.http_client.get("/api/v1/me/datasets").raise_for_status().json()
        json_datasets = response["items"]
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

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_dataset: Dict) -> "DatasetModel":
        json_dataset["inserted_at"] = self._date_from_iso_format(date=json_dataset["inserted_at"])
        json_dataset["updated_at"] = self._date_from_iso_format(date=json_dataset["updated_at"])
        return DatasetModel(**json_dataset)

    def _model_from_jsons(self, json_datasets: List[Dict]) -> List["DatasetModel"]:
        return list(map(self._model_from_json, json_datasets))
