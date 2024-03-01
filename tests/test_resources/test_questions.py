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

import uuid
from unittest.mock import MagicMock

import httpx
import pytest

from argilla_sdk import Dataset
from argilla_sdk.questions import Question, QuestionSettings

class TestQuestionSerialization:
    @pytest.mark.parametrize(
        "settings",
        [
            Question.Settings.Rating(),
            Question.Settings.Rating.from_boundaries(1, 5),
            Question.Settings.Label.from_labels(["label1", "label2"]),
            Question.Settings.MultiLabel.from_labels(["label1"]),
            Question.Settings.Ranking.from_labels(["option1", "option2"]),
            Question.Settings.Text(),
        ],
    )
    def test_serialize(self, settings: QuestionSettings, mock_httpx_client: httpx.Client):
        question = Question(
            name="question",
            title="question",
            description="question",
            required=True,
            settings=settings,
            client=mock_httpx_client,
        )
        assert Question.from_dict(question.to_dict()) == question

class TestQuestions:
    def test_list_questions(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        dataset = Dataset(id=uuid.uuid4(), name="test_dataset", client=mock_httpx_client)

        mock_response.json = mocker.Mock(
            return_value={
                "items": [
                    {
                        "id": "question-01",
                        "name": "question-01",
                        "title": "Question 01",
                        "description": "Question 01 description",
                        "required": True,
                        "settings": {"type": "rating", "options": [{"value": 1}, {"value": 2}]},
                    },
                    {
                        "id": "question-02",
                        "name": "question-02",
                        "title": "Question 02",
                        "description": "Question 02 description",
                        "required": False,
                        "settings": {"type": "text"},
                    },
                ]
            }
        )
        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        questions = dataset.questions.list()
        mock_httpx_client.get.assert_called_once_with(f"/api/v1/datasets/{dataset.id}/questions")

        for question, mock_question in zip(questions, mock_response.json()["items"]):
            assert question.id == mock_question["id"]
            assert question.name == mock_question["name"]
            assert question.title == mock_question["title"]
            assert question.description == mock_question["description"]
            assert question.required == mock_question["required"]
            assert question.settings == Question.Settings.from_dict(mock_question["settings"])
            assert question.client == mock_httpx_client

    def test_get_question_by_id(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        question_id = uuid.uuid4()

        mock_response.json = mocker.Mock(
            return_value={
                "id": question_id,
                "name": "question-01",
                "title": "Question 01",
                "description": "Question 01 description",
                "required": True,
                "settings": {"type": "rating", "options": [{"value": 1}, {"value": 2}]},
            }
        )
        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        question = Question.get(question_id)
        mock_httpx_client.get.assert_called_once_with(f"/api/v1/questions/{question_id}")

        assert question.id == mock_response.json()["id"]
        assert question.name == mock_response.json()["name"]
        assert question.title == mock_response.json()["title"]
        assert question.description == mock_response.json()["description"]
        assert question.required == mock_response.json()["required"]
        assert question.settings == Question.Settings.from_dict(mock_response.json()["settings"])
        assert question.client == mock_httpx_client

    def test_get_question_by_name(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)

        dataset = Dataset(id=uuid.uuid4(), name="test_dataset", client=mock_httpx_client)
        question_name = "question-01"

        mock_response.json = mocker.Mock(
            return_value={
                "items": [
                    {
                        "id": "question-01",
                        "name": question_name,
                        "title": "Question 01",
                        "description": "Question 01 description",
                        "required": True,
                        "settings": {"type": "rating", "options": [{"value": 1}, {"value": 2}]},
                    }
                ]
            }
        )
        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        question = dataset.questions.get_by_name(question_name)
        mock_httpx_client.get.assert_called_once_with(f"/api/v1/datasets/{dataset.id}/questions")

        item_json = mock_response.json()["items"][0]

        assert question.id == item_json["id"]
        assert question.name == item_json["name"]
        assert question.title == item_json["title"]
        assert question.description == item_json["description"]
        assert question.required == item_json["required"]
        assert question.settings == Question.Settings.from_dict(item_json["settings"])
        assert question.client == mock_httpx_client

    def test_create_question(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)

        dataset = Dataset(id=uuid.uuid4(), name="test_dataset", client=mock_httpx_client)
        question = Question(
            name="question-01",
            title="Question 01",
            description="Question 01 description",
            required=True,
            settings=Question.Settings.Rating.from_boundaries(1, 2),
            client=mock_httpx_client,
        )

        mock_response.json = mocker.Mock(
            return_value={
                "id": "question-01",
                "name": "question-01",
                "title": "Question 01",
                "description": "Question 01 description",
                "required": True,
                "settings": {"type": "rating", "options": [{"value": 1}, {"value": 2}]},
            }
        )
        mock_httpx_client.post = mocker.MagicMock(return_value=mock_response)

        created_question = dataset.questions.add(question)
        mock_httpx_client.post.assert_called_once_with(
            f"/api/v1/datasets/{dataset.id}/questions",
            json={
                "name": question.name,
                "title": question.title,
                "description": question.description,
                "required": question.required,
                "settings": question.settings.to_dict(),
            },
        )

        assert created_question.id == mock_response.json()["id"]
        assert created_question.name == mock_response.json()["name"]
        assert created_question.title == mock_response.json()["title"]
        assert created_question.description == mock_response.json()["description"]
        assert created_question.required == mock_response.json()["required"]
        assert created_question.settings == Question.Settings.from_dict(mock_response.json()["settings"])
        assert created_question.client == mock_httpx_client

    def test_update_question(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)

        question_id = uuid.uuid4()
        question = Question(
            id=question_id,
            name="question-01",
            title="Question 01",
            description="Question 01 description",
            required=True,
            settings=Question.Settings.Rating.from_boundaries(1, 2),
            client=mock_httpx_client,
        )

        mock_response.json = mocker.Mock(
            return_value={
                "id": question_id,
                "name": "question-01",
                "title": "Question 01",
                "description": "Question 01 description",
                "required": True,
                "settings": {"type": "rating", "options": [{"value": 1}, {"value": 2}]},
            }
        )
        mock_httpx_client.patch = mocker.MagicMock(return_value=mock_response)

        updated_question = question.update()
        mock_httpx_client.patch.assert_called_once_with(
            f"/api/v1/questions/{question_id}",
            json={
                "title": question.title,
                "description": question.description,
                "settings": question.settings.to_dict(),
            },
        )

        assert updated_question.id == mock_response.json()["id"]
        assert updated_question.name == mock_response.json()["name"]
        assert updated_question.title == mock_response.json()["title"]
        assert updated_question.description == mock_response.json()["description"]
        assert updated_question.required == mock_response.json()["required"]
        assert updated_question.settings == Question.Settings.from_dict(mock_response.json()["settings"])
        assert updated_question.client == mock_httpx_client

    def test_delete_question(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)

        question_id = uuid.uuid4()
        question = Question(
            id=question_id,
            name="question-01",
            title="Question 01",
            description="Question 01 description",
            required=True,
            settings=Question.Settings.Rating.from_boundaries(1, 2),
            client=mock_httpx_client,
        )

        mock_response.json = mocker.Mock(
            return_value={
                "id": question_id,
                "name": "question-01",
                "title": "Question 01",
                "description": "Question 01 description",
                "required": True,
                "settings": {"type": "rating", "options": [{"value": 1}, {"value": 2}]},
            }
        )
        mock_httpx_client.delete = mocker.MagicMock(return_value=mock_response)

        deleted_question = question.delete()
        mock_httpx_client.delete.assert_called_once_with(f"/api/v1/questions/{question_id}")

        assert deleted_question.id == mock_response.json()["id"]
        assert deleted_question.name == mock_response.json()["name"]
        assert deleted_question.title == mock_response.json()["title"]
        assert deleted_question.description == mock_response.json()["description"]
        assert deleted_question.required == mock_response.json()["required"]
        assert deleted_question.settings == Question.Settings.from_dict(mock_response.json()["settings"])
        assert deleted_question.client == mock_httpx_client
