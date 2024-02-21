from pathlib import Path
from tempfile import TemporaryFile
from unittest import mock

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
        assert settings.serialize() == {
            "guidelines": "This is a guideline",
            "fields": [{"name": "prompt", "use_markdown": True}],
            "questions": [{"name": "sentiment", "labels": ["positive", "negative"]}],
        }
