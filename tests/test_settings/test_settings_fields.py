import argilla_sdk as rg


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

    def test_serialize_text_field(self):
        mock_name = "prompt"
        mock_use_markdown = True
        text_field = rg.TextField(name=mock_name, use_markdown=mock_use_markdown)
        serialized = text_field.serialize()
        assert serialized["name"] == mock_name
        assert serialized["use_markdown"] == mock_use_markdown
        assert serialized["required"] == True
