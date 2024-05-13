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

    def test_settings_repr(self):
        settings = rg.Settings(
            fields=[
                rg.TextField(name="text", title="text"),
            ],
            metadata=[
                rg.FloatMetadataProperty("source"),
            ],
            questions=[
                rg.LabelQuestion(name="label", title="text", labels=["positive", "negative"]),
            ],
            vectors=[rg.VectorField(name="text", dimensions=3)],
        )
        
        assert (
            settings.__repr__()
            == f"""Settings(guidelines=None, allow_extra_metadata=False, fields={settings.fields}, questions={settings.questions}, vectors={settings.vectors}, metadata={settings.metadata})"""
        )


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
        assert settings_serialized["fields"][0]["settings"]["use_markdown"] == True