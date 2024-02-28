import pytest
import argilla_sdk as rg

from argilla_sdk.settings.exceptions import InvalidFieldException


class TestTextField:
    def test_init_text_field(self):
        mock_name = "prompt"
        mock_use_markdown = True
        text_field = rg.TextField(name=mock_name, use_markdown=mock_use_markdown)
        assert text_field.name == mock_name
        assert text_field.use_markdown == mock_use_markdown
        assert text_field.title == mock_name
        assert text_field.required == True

    def test_init_text_field_with_title(self):
        mock_name = "prompt"
        mock_use_markdown = True
        mock_title = "Prompt"
        text_field = rg.TextField(name=mock_name, use_markdown=mock_use_markdown, title=mock_title)
        assert text_field.name == mock_name
        assert text_field.use_markdown == mock_use_markdown
        assert text_field.title == mock_title
        assert text_field.required == True

    def test_init_text_field_optional(self):
        mock_name = "prompt"
        mock_use_markdown = True
        mock_required = False
        text_field = rg.TextField(name=mock_name, use_markdown=mock_use_markdown, required=mock_required)
        assert text_field.name == mock_name
        assert text_field.use_markdown == mock_use_markdown
        assert text_field.title == mock_name
        assert text_field.required == mock_required

    @pytest.mark.parametrize(
        "name, expected",
        [
            ("prompt", "prompt"),
            ("Prompt", "prompt"),
            ("Prompt Name", "prompt_name"),
            ("Prompt Name 2", "prompt_name_2"),
            ("Prompt Name 2", "prompt_name_2"),
        ],
    )
    def test_name_validator(self, name, expected, mocker):
        mock_use_markdown = True
        text_field = rg.TextField(name=name, use_markdown=mock_use_markdown)
        assert text_field.name == expected

    @pytest.mark.parametrize(
        "title, name, expected",
        [
            (None, "prompt", "prompt"),
            ("Prompt", "prompt", "Prompt"),
            ("Prompt", "prompt", "Prompt"),
        ],
    )
    def test_title_validator(self, title, name, expected, mocker):
        mock_use_markdown = True
        text_field = rg.TextField(name=name, use_markdown=mock_use_markdown, title=title)
        assert text_field.title == expected

    @pytest.mark.parametrize(
        "name",
        [
            (""),
            (" "),
        ],
    )
    def test_name_validator_exception(self, name, mocker):
        with pytest.raises(InvalidFieldException):
            mock_use_markdown = True
            rg.TextField(name=name, use_markdown=mock_use_markdown)
