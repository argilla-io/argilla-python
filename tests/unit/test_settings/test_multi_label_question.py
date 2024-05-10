import argilla_sdk as rg


class TestMultiLabelQuestions:

    def test_create_question(self):
        question = rg.MultiLabelQuestion(name="span_question", labels=["label1", "label2", "label3"])
        assert question.name == "span_question"
        assert question.labels == ["label1", "label2", "label3"]
        assert question.visible_labels == 3

    def test_change_labels_value(self):
        question = rg.MultiLabelQuestion(name="span_question", labels=["label1", "label2", "label3"])
        question.labels = ["label1", "label2"]
        assert question.labels == ["label1", "label2"]
        assert question.visible_labels == 3

    def test_update_visible_labels(self):
        question = rg.MultiLabelQuestion(name="span_question", labels=["label1", "label2", "label3", "label4"])
        assert question.visible_labels == 4
        question.visible_labels = 3
        assert question.visible_labels == 3
