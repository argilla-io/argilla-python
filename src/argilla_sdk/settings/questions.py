from abc import ABC, abstractmethod
from typing import List


class QuestionBase:
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def serialize(self):
        pass


class LabelQuestion(QuestionBase):
    def __init__(self, name: str, labels: List[str]):
        super().__init__(name)
        self.labels = labels

    def serialize(self):
        return {
            "name": self.name,
            "labels": self.labels,
        }


class RatingQuestion(QuestionBase):
    def __init__(self, name: str, values: List[int]):
        super().__init__(name)
        self.values = values

    def serialize(self):
        return {
            "name": self.name,
            "values": self.values,
        }


class TextQuestion(QuestionBase):
    def __init__(self, name: str, use_markdown: bool = False):
        super().__init__(name)
        self.use_markdown = use_markdown

    def serialize(self):
        return {
            "name": self.name,
            "use_markdown": self.use_markdown,
        }


class MultiLabelQuestion(QuestionBase):
    def __init__(self, name: str, labels: List[str], visible_labels: int = 20):
        super().__init__(name)
        self.labels = labels
        self.visible_labels = visible_labels

    def serialize(self):
        return {
            "name": self.name,
            "labels": self.labels,
            "visible_labels": self.visible_labels,
        }


class RankingQuestion(QuestionBase):
    def __init__(self, name: str, values: List[str]):
        super().__init__(name)
        self.values = values

    def serialize(self):
        return {
            "name": self.name,
            "values": self.values,
        }
