import uuid
from datetime import datetime

import httpx
from pytest_httpx import HTTPXMock

import argilla_sdk as rg


class TestSettings:
    def test_init_settings(self):
        settings = rg.Settings()
        assert settings.fields == []
        assert settings.questions == []

    def test_with_guidelines(self):
        mock_guidelines = "This is a guideline"
        settings = rg.Settings(
            guidelines=mock_guidelines,
        )
        assert settings.guidelines == mock_guidelines

    def test_with_guidelines_attribute(self):
        mock_guidelines = "This is a guideline"
        settings = rg.Settings()
        settings.guidelines = mock_guidelines
        assert settings.guidelines == mock_guidelines

    def test_with_text_field(self):
        mock_name = "prompt"
        mock_use_markdown = True
        settings = rg.Settings(fields=[rg.TextField(name=mock_name, use_markdown=mock_use_markdown)])
        assert settings.fields[0].name == mock_name
        assert settings.fields[0].use_markdown == mock_use_markdown

    def test_with_text_field_attribute(self):
        settings = rg.Settings()
        mock_name = "prompt"
        mock_use_markdown = True
        settings.fields = [rg.TextField(name=mock_name, use_markdown=mock_use_markdown)]
        assert settings.fields[0].name == mock_name
        assert settings.fields[0].use_markdown == mock_use_markdown

    def test_with_label_question(self):
        settings = rg.Settings(questions=[rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])])
        assert settings.questions[0].name == "sentiment"
        assert settings.questions[0].labels == ["positive", "negative"]

    def test_with_label_question_attribute(self):
        settings = rg.Settings()
        settings.questions = [rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])]
        assert settings.questions[0].name == "sentiment"
        assert settings.questions[0].labels == ["positive", "negative"]


class TestSettingsSerialization:
    def test_serialize(self):
        settings = rg.Settings(
            guidelines="This is a guideline",
            fields=[rg.TextField(name="prompt", use_markdown=True)],
            questions=[rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])],
        )
        settings_serialized = settings.serialize()
        assert settings_serialized["guidelines"] == "This is a guideline"
        assert settings_serialized["fields"][0]["name"] == "prompt"
        assert settings_serialized["fields"][0]["use_markdown"] == True


class TestDatasetSettings:
    def test_dataset_init_with_fields_and_questions(self):
        settings = rg.Settings(guidelines="guidelines")
        fields = [rg.TextField(name="prompt", use_markdown=True)]
        questions = [rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])]
        mock_dataset_name = "dataset_name"
        dataset = rg.Dataset(name=mock_dataset_name, settings=settings, fields=fields, questions=questions)

        assert dataset.guidelines == "guidelines"
        assert dataset.fields == fields
        assert dataset.questions == questions

    def test_create_dataset_with_settings(self, httpx_mock: HTTPXMock):
        mock_dataset_name = "dataset_name"
        mock_dataset_id = uuid.uuid4()
        mock_guidelines = "guidelines"
        mock_return_value = {
            "id": str(mock_dataset_id),
            "name": mock_dataset_name,
            "status": "draft",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        with httpx.Client():
            fields = [rg.TextField(name="prompt", use_markdown=True)]
            questions = [rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])]
            settings = rg.Settings(guidelines="guidelines", fields=fields, questions=questions)
            dataset = rg.Dataset(
                name=mock_dataset_name,
                settings=settings,
            )
            client = rg.Argilla(api_url)
            dataset = client.create(dataset)
            assert dataset.guidelines == mock_guidelines
            assert dataset.fields == fields
            assert dataset.questions == questions

    def test_update_dataset_with_guidelines(self, httpx_mock: HTTPXMock):
        mock_dataset_name = "dataset_name"
        mock_dataset_id = uuid.uuid4()
        mock_guidelines = "guidelines"
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": mock_dataset_name,
            "status": "draft",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}",
            method="GET",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        with httpx.Client():
            fields = [rg.TextField(name="prompt", use_markdown=True)]
            questions = [rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])]
            settings = rg.Settings(guidelines=mock_guidelines, fields=fields, questions=questions)
            dataset = rg.Dataset(
                name=mock_dataset_name,
                settings=settings,
                dataset_id=mock_dataset_id,
            )
            client = rg.Argilla(api_url)
            dataset = client.create(dataset)
            gotten_dataset = client.get(dataset)
            gotten_dataset.guidelines = "new guidelines"
            dataset = client.update(dataset)
            assert dataset.guidelines == "new guidelines"
            assert dataset.fields == fields
            assert dataset.questions == questions

    def test_update_dataset_with_new_fields(self, httpx_mock: HTTPXMock):
        mock_dataset_name = "dataset_name"
        mock_dataset_id = uuid.uuid4()
        mock_guidelines = "guidelines"
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": mock_dataset_name,
            "status": "draft",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}",
            method="GET",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        with httpx.Client():
            fields = [rg.TextField(name="prompt", use_markdown=True)]
            updated_fields = [rg.TextField(name="new_prompt", use_markdown=True)]
            questions = [rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])]
            settings = rg.Settings(guidelines=mock_guidelines, fields=fields, questions=questions)
            dataset = rg.Dataset(
                name=mock_dataset_name,
                settings=settings,
                dataset_id=mock_dataset_id,
            )
            client = rg.Argilla(api_url)
            dataset = client.create(dataset)
            gotten_dataset = client.get(dataset)
            gotten_dataset.fields = updated_fields
            dataset = client.update(dataset)
            assert dataset.guidelines == mock_guidelines
            assert dataset.fields == updated_fields
            assert dataset.questions == questions

    def test_update_dataset_with_new_questions(self, httpx_mock: HTTPXMock):
        mock_dataset_name = "dataset_name"
        mock_dataset_id = uuid.uuid4()
        mock_guidelines = "guidelines"
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": mock_dataset_name,
            "status": "draft",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}",
            method="GET",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        with httpx.Client():
            fields = [rg.TextField(name="prompt", use_markdown=True)]
            questions = [rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])]
            updated_questions = [rg.LabelQuestion(name="new_sentiment", labels=["positive", "negative"])]
            settings = rg.Settings(guidelines=mock_guidelines, fields=fields, questions=questions)
            dataset = rg.Dataset(
                name=mock_dataset_name,
                settings=settings,
                dataset_id=mock_dataset_id,
            )
            client = rg.Argilla(api_url)
            dataset = client.create(dataset)
            gotten_dataset = client.get(dataset)
            gotten_dataset.questions = updated_questions
            dataset = client.update(dataset)
            assert dataset.guidelines == mock_guidelines
            assert dataset.fields == fields
            assert dataset.questions == updated_questions

    def test_update_dataset_with_allow_extra_metadata(self, httpx_mock):
        mock_dataset_name = "dataset_name"
        mock_dataset_id = uuid.uuid4()
        mock_guidelines = "guidelines"
        mock_create_return_value = {
            "id": mock_dataset_id.hex,
            "name": mock_dataset_name,
            "status": "draft",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        mock_update_return_value = {
            "id": mock_dataset_id.hex,
            "name": mock_dataset_name,
            "status": "draft",
            "allow_extra_metadata": True,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_update_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_create_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}",
            method="GET",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_create_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        with httpx.Client():
            fields = [rg.TextField(name="prompt", use_markdown=True)]
            questions = [rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])]
            settings = rg.Settings(guidelines=mock_guidelines, fields=fields, questions=questions, allow_extra_metadata=True)
            dataset = rg.Dataset(
                name=mock_dataset_name,
                settings=settings,
                dataset_id=mock_dataset_id,
            )
            client = rg.Argilla(api_url)
            dataset = client.create(dataset)
            gotten_dataset = client.get(dataset)
            gotten_dataset.allow_extra_metadata = True
            updated_dataset = client.update(dataset)
            assert updated_dataset.guidelines == mock_guidelines
            assert updated_dataset.fields == fields
            assert updated_dataset.questions == questions
            assert updated_dataset.allow_extra_metadata is True