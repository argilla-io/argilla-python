import uuid

import argilla_sdk as rg
from argilla_sdk._models import MetadataFieldModel, TermsMetadataPropertySettings


class TestTermsMetadata:

    def test_create_metadata_terms(self):
        property = rg.TermsMetadataProperty(
            title="A metadata property", name="metadata", options=["option1", "option2"]
        )

        assert property._model.type == "terms"
        assert property.title == "A metadata property"
        assert property.name == "metadata"
        assert property.visible_for_annotators is True
        assert property.options == ["option1", "option2"]

        assert property.api_model().model_dump() == {
            "id": None,
            "name": "metadata",
            "settings": {"type": "terms", "values": ["option1", "option2"], "visible_for_annotators": True},
            "title": "A metadata property",
            "type": "terms",
            "visible_for_annotators": True,
        }

    def test_create_terms_metadata_without_options(self):
        property = rg.TermsMetadataProperty(name="metadata")

        assert property.title == "metadata"
        assert property.name == "metadata"
        assert property.visible_for_annotators is True
        assert property.options is None

        model = property.api_model()
        assert model.type == "terms"
        assert model.model_dump() == {
            "id": None,
            "name": "metadata",
            "title": "metadata",
            "settings": {"type": "terms", "values": None, "visible_for_annotators": True},
            "type": "terms",
            "visible_for_annotators": True,
        }

    def test_create_from_model(self):
        model = MetadataFieldModel(
            id=uuid.uuid4(),
            name="metadata",
            title="A metadata property",
            type="terms",
            settings=TermsMetadataPropertySettings(values=["option1", "option2"], type="terms"),
            visible_for_annotators=True,
        )

        property = rg.TermsMetadataProperty.from_model(model)

        assert property.id == model.id
        assert property.title == "A metadata property"
        assert property.name == "metadata"
        assert property.visible_for_annotators is True
        assert property.options == ["option1", "option2"]
