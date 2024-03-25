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

from typing import List, Dict, Union
from uuid import UUID

import httpx
from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceAPI
from argilla_sdk._models import (
    TextQuestionModel,
    LabelQuestionModel,
    MultiLabelQuestionModel,
    RankingQuestionModel,
    RatingQuestionModel,
    QuestionBaseModel,
)

__all__ = ["QuestionsAPI"]


class QuestionsAPI(ResourceAPI[QuestionBaseModel]):
    """Manage datasets via the API"""

    http_client: httpx.Client

    ################
    # CRUD methods #
    ################

    def create(
        self,
        dataset_id: UUID,
        question: Union[
            TextQuestionModel,
            LabelQuestionModel,
            MultiLabelQuestionModel,
            RankingQuestionModel,
            RatingQuestionModel,
            QuestionBaseModel,
        ],
    ) -> Union[
        TextQuestionModel,
        LabelQuestionModel,
        MultiLabelQuestionModel,
        RankingQuestionModel,
        RatingQuestionModel,
        QuestionBaseModel,
    ]:
        url = f"/api/v1/datasets/{dataset_id}/questions"
        response = self.http_client.post(url=url, json=question.model_dump())
        _http.raise_for_status(response=response)
        question_model = self._model_from_json(response_json=response.json())
        self.log(message=f"Created question {question_model.name} in dataset {dataset_id}")
        return question_model

    def update(
        self,
        question: Union[
            TextQuestionModel,
            LabelQuestionModel,
            MultiLabelQuestionModel,
            RankingQuestionModel,
            RatingQuestionModel,
            QuestionBaseModel,
        ],
    ) -> Union[
        TextQuestionModel,
        LabelQuestionModel,
        MultiLabelQuestionModel,
        RankingQuestionModel,
        RatingQuestionModel,
        QuestionBaseModel,
    ]:
        # TODO: Implement update method for fields with server side ID
        raise NotImplementedError

    def delete(self, question_id: UUID) -> None:
        # TODO: Implement delete method for fields with server side ID
        raise NotImplementedError

    ####################
    # Utility methods #
    ####################

    def create_many(
        self, dataset_id: UUID, questions: List[Dict]
    ) -> List[
        Union[
            TextQuestionModel,
            LabelQuestionModel,
            MultiLabelQuestionModel,
            RankingQuestionModel,
            RatingQuestionModel,
            QuestionBaseModel,
        ]
    ]:
        response_models = []
        for question in questions:
            response_model = self.create(dataset_id=dataset_id, question=question)
            response_models.append(response_model)
        return response_models

    def list(
        self, dataset_id: UUID
    ) -> List[
        Union[
            TextQuestionModel,
            LabelQuestionModel,
            MultiLabelQuestionModel,
            RankingQuestionModel,
            RatingQuestionModel,
            QuestionBaseModel,
        ]
    ]:
        response = self.http_client.get(f"/api/v1/datasets/{dataset_id}/questions")
        _http.raise_for_status(response=response)
        response_models = self._model_from_jsons(response_jsons=response.json()["items"])
        return response_models

    ####################
    # Private methods #
    ####################

    def _model_from_json(
        self, response_json: Dict
    ) -> Union[
        TextQuestionModel,
        LabelQuestionModel,
        MultiLabelQuestionModel,
        RankingQuestionModel,
        RatingQuestionModel,
        QuestionBaseModel,
    ]:
        response_json["inserted_at"] = self._date_from_iso_format(date=response_json["inserted_at"])
        response_json["updated_at"] = self._date_from_iso_format(date=response_json["updated_at"])
        return self._get_model_from_response(response_json=response_json)

    def _model_from_jsons(
        self, response_jsons: List[Dict]
    ) -> List[
        Union[
            TextQuestionModel,
            LabelQuestionModel,
            MultiLabelQuestionModel,
            RankingQuestionModel,
            RatingQuestionModel,
            QuestionBaseModel,
        ]
    ]:
        return list(map(self._model_from_json, response_jsons))

    def _get_model_from_response(
        self, response_json: Dict
    ) -> Union[
        TextQuestionModel,
        LabelQuestionModel,
        MultiLabelQuestionModel,
        RankingQuestionModel,
        RatingQuestionModel,
        QuestionBaseModel,
    ]:
        try:
            question_type = response_json.get("settings", {}).get("type")
        except Exception as e:
            raise ValueError("Invalid field type: missing 'settings.type' in response") from e
        if question_type == "text":
            return TextQuestionModel(**response_json)
        elif question_type == "label_selection":
            return LabelQuestionModel(**response_json)
        elif question_type == "multi_label_selection":
            return MultiLabelQuestionModel(**response_json)
        elif question_type == "ranking":
            return RankingQuestionModel(**response_json)
        elif question_type == "rating":
            return RatingQuestionModel(**response_json)
        else:
            self.log(message=f"Unknown question type: {question_type}")
            return QuestionBaseModel(**response_json)
