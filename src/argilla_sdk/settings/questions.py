from typing import List
from pydantic import BaseModel


class QuestionBase(BaseModel):
    name: str

    class Config:
        validate_assignment = True


class LabelQuestion(QuestionBase):
    labels: List[str]


class RatingQuestion(QuestionBase):
    values: List[int]


class TextQuestion(QuestionBase):
    use_markdown: bool


class MultiLabelQuestion(QuestionBase):
    labels: List[str]
    visible_labels: int


class RankingQuestion(QuestionBase):
    values: List[int]
