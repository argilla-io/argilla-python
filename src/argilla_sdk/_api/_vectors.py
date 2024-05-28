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

from argilla_sdk._api._base import ResourceAPI
from argilla_sdk._exceptions import api_error_handler
from argilla_sdk._models import VectorFieldModel

__all__ = ["VectorsAPI"]


class VectorsAPI(ResourceAPI[VectorFieldModel]):
    """Manage vectors via the API"""

    http_client: httpx.Client

    ################
    # CRUD methods #
    ################

    @api_error_handler
    def create(self, vector_model: VectorFieldModel) -> VectorFieldModel:
        url = f"/api/v1/datasets/{vector_model.dataset_id}/vectors-settings"
        response = self.http_client.post(url=url, json=vector_model.model_dump())
        response.raise_for_status()
        response_json = response.json()
        model_created = self._model_from_json(response_json=response_json)
        self.log(message=f"Created vector {model_created.name} in dataset {model_created.dataset_id}")
        return model_created

    @api_error_handler
    def update(self, vector_model: VectorFieldModel) -> VectorFieldModel:
        url = f"/api/v1/vectors-settings/{vector_model.id}"
        response = self.http_client.patch(url, json=vector_model.model_dump())
        response.raise_for_status()
        response_json = response.json()
        model_updated = self._model_from_json(response_json)
        self.log(message=f"Updated vector {model_updated.name} with id {model_updated.id}")
        return model_updated

    @api_error_handler
    def delete(self, vector_id: UUID) -> None:
        url = f"/api/v1/vectors-settings/{vector_id}"
        response = self.http_client.delete(url)
        response.raise_for_status()
        self.log(message=f"Deleted vector with id {vector_id}")

    ####################
    # Utility methods #
    ####################

    @api_error_handler
    def list(self, dataset_id: UUID) -> List[VectorFieldModel]:
        response = self.http_client.get(f"/api/v1/datasets/{dataset_id}/vectors-settings")
        response.raise_for_status()
        response_json = response.json()
        vector_models = self._model_from_jsons(response_jsons=response_json["items"])
        return vector_models

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, response_json: Dict) -> VectorFieldModel:
        response_json["inserted_at"] = self._date_from_iso_format(date=response_json["inserted_at"])
        response_json["updated_at"] = self._date_from_iso_format(date=response_json["updated_at"])
        return VectorFieldModel(**response_json)

    def _model_from_jsons(self, response_jsons: List[Dict]) -> List[VectorFieldModel]:
        return list(map(self._model_from_json, response_jsons))
