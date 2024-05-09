import argilla_sdk as rg


class TestMetadataSettings:

    def test_create_metadata_terms(self):
        property = rg.TermsMetadataProperty(
            title="A metadata property", name="metadata", options=["option1", "option2"]
        )

        assert property._model.type == "terms"
        assert property.title == "A metadata property"
        assert property.name == "metadata"
        assert property.visible_for_annotators is True
        assert property.options == ["option1", "option2"]

        assert property._model.dict() == {
            "id": None,
            "name": "metadata",
            "settings": {"type": "terms", "values": ["option1", "option2"], "visible_for_annotators": True},
            "title": "A metadata property",
            "type": "terms",
            "visible_for_annotators": True,
        }
