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

import datetime
from dataclasses import dataclass, field
from typing import List, Literal, Optional
from uuid import UUID

import httpx

import argilla_sdk
from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceBase
from argilla_sdk.datasets import Dataset

__all__ = ["DatasetsAPI"]


class DatasetsAPI(ResourceBase):
    """Manage datasets via the API"""

    http_client: Optional[httpx.Client] = field(default=None, repr=False, compare=False)

    ################
    # CRUD methods #
    ################

    def create(self, dataset: Dataset) -> "Dataset":
        json_body = {
            "name": dataset.name,
            "workspace_id": dataset.workspace_id,
            "guidelines": dataset.guidelines,
            "allow_extra_metadata": dataset.allow_extra_metadata,
        }
        response = self.http_client.post(
            "/api/v1/datasets",
            json=json_body,
        )
        _http.raise_for_status(response)
        self.log(f"Created dataset {dataset.name}")

    def update(self, dataset: Dataset) -> None:
        json_body = {
            "guidelines": dataset.guidelines,
            "allow_extra_metadata": dataset.allow_extra_metadata,
        }
        response = self.http_client.patch(f"/api/v1/datasets/{dataset.id}", json=json_body)
        _http.raise_for_status(response)
        self.log(f"Updated dataset {dataset.name}")

    def get(self, dataset_id: UUID) -> "Dataset":
        response = self.http_client.get(f"/api/v1/datasets/{dataset_id}")
        _http.raise_for_status(response)
        json_dataset = response.json()
        dataset = self._model_from_json(json_dataset)
        self.log(f"Got dataset {dataset.name}")
        return dataset

    def delete(self, dataset_id: UUID) -> "Dataset":
        response = self.http_client.delete(f"/api/v1/datasets/{dataset_id}")
        _http.raise_for_status(response)
        self.log(f"Deleted dataset {dataset_id}")

    ####################
    # Utility methods #
    ####################

    def publish(self, dataset_id) -> None:
        response = self.http_client.put(f"/api/v1/datasets/{dataset_id}/publish")
        _http.raise_for_status(response)
        self.log(f"Published dataset {dataset_id}")

    def list(self, workspace_id: Optional[UUID] = None) -> List["Dataset"]:
        response = self.http_client.get("/api/v1/me/datasets")
        _http.raise_for_status(response)
        json_datasets = response.json()["items"]
        datasets = self._model_from_jsons(json_datasets)
        if workspace_id:
            datasets = [dataset for dataset in datasets if dataset.workspace_id == workspace_id]
        self.log(f"Listed {len(datasets)} datasets")
        return datasets

    def get_by_name_and_workspace_id(self, name: str, workspace_id: UUID) -> Optional["Dataset"]:
        datasets = self.list(workspace_id=workspace_id)
        for dataset in datasets:
            if dataset.name == name:
                self.log(f"Got dataset {dataset.name}")
                return dataset

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_dataset: dict) -> "Dataset":
        return Dataset(
            name=json_dataset["name"],
            status=json_dataset["status"],
            guidelines=json_dataset["guidelines"],
            allow_extra_metadata=json_dataset["allow_extra_metadata"],
            id=UUID(json_dataset["id"]),
            workspace_id=UUID(json_dataset["workspace_id"]),
            inserted_at=self._date_from_iso_format(json_dataset["inserted_at"]),
            updated_at=self._date_from_iso_format(json_dataset["updated_at"]),
        )

    def _model_from_jsons(self, json_datasets: List[dict]) -> List["Dataset"]:
        return list(map(self._model_from_json, json_datasets))
