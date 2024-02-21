from typing import List


class QuestionBase:
    pass


class LabelQuestion(QuestionBase):
    def __init__(self, name: str, labels: List[str]):
        self.name = name
        self.labels = labels

    def serialize(self):
        return {
            "name": self.name,
            "labels": self.labels,
        }
