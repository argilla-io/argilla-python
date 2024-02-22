import argilla_sdk as rg


class TestQuestions:
    def test_label_question_init(self):
        question = rg.LabelQuestion("label_question", ["label1", "label2"])
        assert question.name == "label_question"
        assert question.labels == ["label1", "label2"]

    def test_rating_question_init(self):
        question = rg.RatingQuestion("rating_question", [1, 2, 3])
        assert question.name == "rating_question"
        assert question.values == [1, 2, 3]

    def test_text_question_init(self):
        question = rg.TextQuestion("text_question", True)
        assert question.name == "text_question"
        assert question.use_markdown == True

    def test_multi_label_question_init(self):
        question = rg.MultiLabelQuestion("multi_label_question", ["label1", "label2"], 2)
        assert question.name == "multi_label_question"
        assert question.labels == ["label1", "label2"]
        assert question.visible_labels == 2

    def test_ranking_question_init(self):
        question = rg.RankingQuestion("ranking_question", ["value1", "value2"])
        assert question.name == "ranking_question"
        assert question.values == ["value1", "value2"]


class TestQuestionSerialization:
    def test_label_question_serialize(self):
        question = rg.LabelQuestion("label_question", ["label1", "label2"])
        assert question.serialize() == {"name": "label_question", "labels": ["label1", "label2"]}

    def test_rating_question_serialize(self):
        question = rg.RatingQuestion("rating_question", [1, 2, 3])
        assert question.serialize() == {"name": "rating_question", "values": [1, 2, 3]}

    def test_text_question_serialize(self):
        question = rg.TextQuestion("text_question", True)
        assert question.serialize() == {"name": "text_question", "use_markdown": True}

    def test_multi_label_question_serialize(self):
        question = rg.MultiLabelQuestion("multi_label_question", ["label1", "label2"], 2)
        assert question.serialize() == {
            "name": "multi_label_question",
            "labels": ["label1", "label2"],
            "visible_labels": 2,
        }

    def test_ranking_question_serialize(self):
        question = rg.RankingQuestion("ranking_question", ["value1", "value2"])
        assert question.serialize() == {"name": "ranking_question", "values": ["value1", "value2"]}
