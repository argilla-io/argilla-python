from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class QuestionBase(ABC):
    name: str

    @abstractmethod
    def serialize(self):
        pass


@dataclass
class LabelQuestion(QuestionBase):
    labels: List[str]

    def serialize(self):
        return {
            "name": self.name,
            "labels": self.labels,
        }


@dataclass
class RatingQuestion(QuestionBase):
    values: List[str]

    def serialize(self):
        return {
            "name": self.name,
            "values": self.values,
        }


@dataclass
class TextQuestion(QuestionBase):
    use_markdown: bool

    def serialize(self):
        return {
            "name": self.name,
            "use_markdown": self.use_markdown,
        }


@dataclass
class MultiLabelQuestion(QuestionBase):
    labels: List[str]
    visible_labels: int

    def serialize(self):
        return {
            "name": self.name,
            "labels": self.labels,
            "visible_labels": self.visible_labels,
        }


@dataclass
class RankingQuestion(QuestionBase):
    values: List[str]

    def serialize(self):
        return {
            "name": self.name,
            "values": self.values,
        }
