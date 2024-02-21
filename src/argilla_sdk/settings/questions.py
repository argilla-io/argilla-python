from typing import List
from pydantic import BaseModel


class QuestionBase(BaseModel):
    name: str

    class Config:
        validate_assignment = True


class LabelQuestion(QuestionBase):
    labels: List[str]


@dataclass
class RatingQuestion(QuestionBase):
    values: List[int]


class TextQuestion(QuestionBase):
    use_markdown: bool


@dataclass
class MultiLabelQuestion(QuestionBase):
    labels: List[str]
    visible_labels: int


@dataclass
class RankingQuestion(QuestionBase):
    values: List[int]
