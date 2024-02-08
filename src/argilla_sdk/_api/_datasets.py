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

__all__ = ["Dataset"]


@dataclass
class Dataset:
    name: str
    status: Literal["draft", "ready"] = "draft"
    guidelines: Optional[str] = None
    allow_extra_metadata: bool = True

    id: Optional[UUID] = None
    workspace_id: Optional[UUID] = None
    inserted_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    last_activity_at: Optional[datetime.datetime] = None

    client: Optional[httpx.Client] = field(default=None, repr=False, compare=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "guidelines": self.guidelines,
            "allow_extra_metadata": self.allow_extra_metadata,
            "workspace_id": self.workspace_id,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Dataset":
        return cls(**data)

    @classmethod
    def list(cls, workspace_id: Optional[UUID] = None) -> List["Dataset"]:
        client = argilla_sdk.get_default_http_client()

        response = client.get("/api/v1/me/datasets")
        _http.raise_for_status(response)

        json_response = response.json()
        datasets = [cls._create_from_json(json_dataset, client) for json_dataset in json_response["items"]]

        if workspace_id:
            datasets = [dataset for dataset in datasets if dataset.workspace_id == workspace_id]

        return datasets

    @classmethod
    def get(cls, dataset_id: UUID) -> "Dataset":
        client = argilla_sdk.get_default_http_client()

        response = client.get(f"/api/v1/datasets/{dataset_id}")
        _http.raise_for_status(response)

        return cls._create_from_json(response.json(), client)

    @classmethod
    def get_by_name_and_workspace_id(cls, name: str, workspace_id: UUID) -> Optional["Dataset"]:
        datasets = cls.list(workspace_id=workspace_id)

        for dataset in datasets:
            if dataset.name == name:
                return dataset

    def create(self) -> "Dataset":
        body = {
            "name": self.name,
            "workspace_id": self.workspace_id,
            "guidelines": self.guidelines,
            "allow_extra_metadata": self.allow_extra_metadata,
        }

        response = self.client.post("/api/v1/datasets", json=body)
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def update(self) -> "Dataset":
        body = {
            "guidelines": self.guidelines,
            "allow_extra_metadata": self.allow_extra_metadata,
        }
        
        response = self.client.patch(f"/api/v1/datasets/{self.id}", json=body)
        
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def delete(self) -> "Dataset":
        response = self.client.delete(f"/api/v1/datasets/{self.id}")
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def publish(self) -> "Dataset":
        response = self.client.put(f"/api/v1/datasets/{self.id}/publish")
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    @classmethod
    def _create_from_json(cls, json: dict, client: httpx.Client) -> "Dataset":
        return cls.from_dict(dict(**json, client=client))

    def _update_from_api_response(self, response: httpx.Response) -> "Dataset":
        new_instance = self._create_from_json(response.json(), client=self.client)
        self.__dict__.update(new_instance.__dict__)
        
        return self
