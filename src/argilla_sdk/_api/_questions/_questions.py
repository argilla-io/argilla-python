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
from typing import Any, ClassVar, Dict, List, Optional, Type
from uuid import UUID

import httpx

import argilla_sdk
from argilla_sdk._api import _http
from argilla_sdk._api._questions._settings import QuestionSettings, SettingsType  # noqa

__all__ = ["Question"]


@dataclass
class Question:
    Settings: ClassVar[Type[SettingsType]] = SettingsType

    name: str
    title: str
    settings: QuestionSettings
    required: bool = True
    description: Optional[str] = None

    id: Optional[UUID] = None
    dataset_id: Optional[UUID] = None
    inserted_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    client: Optional[httpx.Client] = field(default=None, repr=False, compare=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "required": self.required,
            "settings": self.settings.to_dict(),
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
            "dataset_id": self.dataset_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        data_copy = data.copy()
        settings = SettingsType.from_dict(data_copy.pop("settings"))

        return cls(**data_copy, settings=settings)

    @classmethod
    def list_by_dataset_id(cls, dataset_id: UUID) -> List["Question"]:
        client = argilla_sdk.get_default_http_client()

        response = client.get(f"/api/v1/datasets/{dataset_id}/questions")
        response.raise_for_status()

        json_response = response.json()
        return [cls._create_from_json(json_question, client) for json_question in json_response["items"]]

    @classmethod
    def get(cls, question_id: UUID) -> "Question":
        client = argilla_sdk.get_default_http_client()

        response = client.get(f"/api/v1/questions/{question_id}")
        response.raise_for_status()

        return cls._create_from_json(response.json(), client)

    @classmethod
    def get_by_name(cls, dataset_id: UUID, name: str) -> "Question":
        # TODO: Maybe we should support an query parameter for this?
        questions = cls.list_by_dataset_id(dataset_id)
        for question in questions:
            if question.name == name:
                return question

    def create(self) -> "Question":
        body = {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "required": self.required,
            "settings": self.settings.to_dict(),
        }

        response = self.client.post(f"/api/v1/datasets/{self.dataset_id}/questions", json=body)
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def update(self) -> "Question":
        body = {
            "title": self.title,
            "description": self.description,
            "settings": self.settings.to_dict(),
        }

        response = self.client.patch(f"/api/v1/questions/{self.id}", json=body)
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def delete(self) -> "Question":
        response = self.client.delete(f"/api/v1/questions/{self.id}")
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    @classmethod
    def _create_from_json(cls, json: Dict[str, Any], client: httpx.Client) -> "Question":
        return cls.from_dict(dict(**json, client=client))

    def _update_from_api_response(self, response: httpx.Response) -> "Question":
        new_instance = self._create_from_json(response.json(), client=self.client)
        self.__dict__.update(new_instance.__dict__)

        return self
