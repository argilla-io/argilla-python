import argilla_sdk as rg


class TestQuestions:
    def test_label_question_init(self):
        question = rg.LabelQuestion(name="label_question", labels=["label1", "label2"])
        assert question.name == "label_question"
        assert question.labels == ["label1", "label2"]

    def test_rating_question_init(self):
        question = rg.RatingQuestion(name="rating_question", values=[1, 2, 3])
        assert question.name == "rating_question"
        assert question.values == [1, 2, 3]

    def test_text_question_init(self):
        question = rg.TextQuestion(name="text_question", use_markdown=True)
        assert question.name == "text_question"
        assert question.use_markdown == True

    def test_multi_label_question_init(self):
        question = rg.MultiLabelQuestion(name="multi_label_question", labels=["label1", "label2"], visible_labels=2)
        assert question.name == "multi_label_question"
        assert question.labels == ["label1", "label2"]
        assert question.visible_labels == 2

    def test_ranking_question_init(self):
        question = rg.RankingQuestion(name="ranking_question", values=[1, 2])
        assert question.name == "ranking_question"
        assert question.values == [1, 2]
