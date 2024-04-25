from typing import List, Optional, Dict, Union

from argilla_sdk._models import (
    LabelQuestionModel,
    LabelQuestionSettings,
    MultiLabelQuestionModel,
    RankingQuestionModel,
    TextQuestionModel,
    TextQuestionSettings,
    QuestionSettings,
    RatingQuestionModel,
    QuestionModel,
)
from argilla_sdk._models._settings._questions import SpanQuestionSettings, SpanQuestionModel
from argilla_sdk.settings._common import SettingsPropertyBase

__all__ = [
    "LabelQuestion",
    "MultiLabelQuestion",
    "RankingQuestion",
    "TextQuestion",
    "RatingQuestion",
    "SpanQuestion",
    "QuestionType",
]


class LabelQuestion(SettingsPropertyBase):
    _model: LabelQuestionModel

    def __init__(
        self,
        name: str,
        labels: List[str],
        title: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = True,
    ) -> None:
        """Create a new label question for `Settings` of a `Dataset`
        Args:
            name: str: The name of the question to be used as a reference.
            labels: List[str]: The list of available labels for the question.
            title: Optional[str]: The title of the question to be shown in the UI.
            description: Optional[str]: The description of the question to be shown in the UI.
            required: bool: If the question is required for a record to be valid.
        """
        self._model = LabelQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            settings=LabelQuestionSettings(options=self._render_labels_as_options(labels), type="label_selection"),
        )

    @classmethod
    def from_model(cls, model: LabelQuestionModel) -> "LabelQuestion":
        instance = cls(
            name=model.name,
            labels=[option["value"] for option in model.settings.options],
        )
        instance._model = model
        return instance

    ##############################
    # Public properties
    ##############################

    @property
    def labels(self) -> List[str]:
        return [option["value"] for option in self._model.settings.options]

    @labels.setter
    def labels(self, labels: List[str]) -> None:
        self._model.settings.options = self._render_labels_as_options(labels)

    ##############################
    # Private methods
    ##############################

    def _render_labels_as_options(
        self, labels: Union[List[str], List[Dict[str, Optional[str]]]]
    ) -> List[Dict[str, str]]:
        """Render labels as options for the question so that the model conforms to the API schema"""
        if isinstance(labels, list) and all(isinstance(label, str) for label in labels):
            return [{"text": label, "value": label} for label in labels]
        elif (
            isinstance(labels, list)
            and all(isinstance(label, dict) for label in labels)
            and all("value" in label and "text" in label for label in labels)
        ):
            return labels
        else:
            raise ValueError("Invalid labels format. Please provide a list of strings or a list of dictionaries.")


class TextQuestion(SettingsPropertyBase):
    _model: TextQuestionModel

    def __init__(
        self,
        name: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = True,
        use_markdown: bool = False,
    ) -> None:
        """Create a new text question for `Settings` of a `Dataset`
        Args:
            name: str: The name of the question to be used as a reference.
            title: Optional[str]: The title of the question to be shown in the UI.
            description: Optional[str]: The description of the question to be shown in the UI.
            required: bool: If the question is required for a record to be valid.
            use_markdown: bool: If the question should use markdown for the description.
        """
        self._model = TextQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            settings=TextQuestionSettings(use_markdown=use_markdown, type="text"),
        )

    @classmethod
    def from_model(cls, model: TextQuestionModel) -> "TextQuestion":
        instance = cls(name=model.name)
        instance._model = model

        return instance

    @property
    def use_markdown(self) -> bool:
        return self._model.settings.use_markdown


class MultiLabelQuestion(LabelQuestion):
    _model: MultiLabelQuestionModel

    def __init__(
        self,
        name: str,
        labels: List[str],
        visible_labels: Optional[int] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = True,
    ) -> None:
        """Create a new multilabel question for `Settings` of a `Dataset`
        Args:
            name: str: The name of the question to be used as a reference.
            labels: List[str]: The list of available labels for the question.
            title: Optional[str]: The title of the question to be shown in the UI.
            description: Optional[str]: The description of the question to be shown in the UI.
            required: bool: If the question is required for a record to be valid.
        """
        self._model = MultiLabelQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            visible_labels=visible_labels,
            settings=LabelQuestionSettings(
                options=self._render_labels_as_options(labels), type="multi_label_selection"
            ),
        )

    @classmethod
    def from_model(cls, model: MultiLabelQuestionModel) -> "MultiLabelQuestion":
        instance = cls(name=model.name, labels=[option["value"] for option in model.settings.options])
        instance._model = model

        return instance

    @property
    def visible_labels(self) -> Optional[int]:
        return self._model.visible_labels

    @visible_labels.setter
    def visible_labels(self, visible_labels: Optional[int]) -> None:
        self._model.visible_labels = visible_labels

    @property
    def labels(self) -> List[str]:
        return [option["value"] for option in self._model.settings.options]

    @labels.setter
    def labels(self, labels: List[str]) -> None:
        self._model.settings.options = self._render_labels_as_options(labels)


class RatingQuestion(SettingsPropertyBase):
    _model: RatingQuestionModel

    def __init__(
        self,
        name: str,
        values: List[int],
        title: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = True,
    ) -> None:
        """Create a new rating question for `Settings` of a `Dataset`
        Args:
            name: str: The name of the question to be used as a reference.
            values: List[int]: The list of available values for the question.
            title: Optional[str]: The title of the question to be shown in the UI.
            description: Optional[str]: The description of the question to be shown in the UI.
            required: bool: If the question is required for a record to be valid.
        """
        self._model = RatingQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            values=values,
            settings=QuestionSettings(type="rating"),
        )

    @classmethod
    def from_model(cls, model: RatingQuestionModel) -> "RatingQuestion":
        instance = cls(name=model.name)
        instance._model = model

        return instance

    @property
    def values(self) -> List[int]:
        return self._model.values

    @values.setter
    def values(self, values: List[int]) -> None:
        self._model.values = values


class RankingQuestion(SettingsPropertyBase):
    _model: RankingQuestionModel

    def __init__(
        self,
        name: str,
        values: List[int],
        title: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = True,
    ) -> None:
        """Create a new ranking question for `Settings` of a `Dataset`
        Args:
            name: str: The name of the question to be used as a reference.
            values: List[int]: The list of available values for the question.
            title: Optional[str]: The title of the question to be shown in the UI.
            description: Optional[str]: The description of the question to be shown in the UI.
            required: bool: If the question is required for a record to be valid.
        """
        self._model = RankingQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            values=values,
            settings=QuestionSettings(type="ranking"),
        )

    @classmethod
    def from_model(cls, model: RankingQuestionModel) -> "RankingQuestion":
        instance = cls(name=model.name, values=model.values)
        instance._model = model

        return instance

    @property
    def values(self) -> List[int]:
        return self._model.values

    @values.setter
    def values(self, values: List[int]) -> None:
        self._model.values = values


class SpanQuestion(MultiLabelQuestion):
    _model: SpanQuestionModel

    def __init__(
        self,
        name: str,
        field: str,
        labels: List[str],
        allow_overlapping: bool = False,
        visible_labels: Optional[int] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = True,
    ):
        self._model = SpanQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            settings=SpanQuestionSettings(
                field=field,
                allow_overlapping=allow_overlapping,
                visible_options=visible_labels,
                options=self._render_labels_as_options(labels),
            ),
        )

    @property
    def name(self):
        return self._model.name

    @property
    def field(self):
        return self._model.settings.field

    @field.setter
    def field(self, field: str):
        self._model.settings.field = field

    @property
    def allow_overlapping(self):
        return self._model.settings.allow_overlapping

    @allow_overlapping.setter
    def allow_overlapping(self, allow_overlapping: bool):
        self._model.settings.allow_overlapping = allow_overlapping

    @property
    def visible_labels(self) -> Optional[int]:
        return self._model.settings.visible_options

    @visible_labels.setter
    def visible_labels(self, visible_labels: Optional[int]) -> None:
        self._model.settings.visible_options = visible_labels

    @property
    def labels(self) -> List[str]:
        return [option["value"] for option in self._model.settings.options]

    @labels.setter
    def labels(self, labels: List[str]) -> None:
        self._model.settings.options = self._render_labels_as_options(labels)

    @classmethod
    def from_model(cls, model: SpanQuestionModel) -> "MultiLabelQuestion":
        instance = cls(
            name=model.name,
            field=model.settings.field,
            labels=[option["value"] for option in model.settings.options],
        )
        instance._model = model

        return instance


QuestionType = Union[
    LabelQuestion,
    MultiLabelQuestion,
    RankingQuestion,
    TextQuestion,
    RatingQuestion,
    SpanQuestion,
]

_TYPE_TO_CLASS = {
    "label_selection": LabelQuestion,
    "multi_label_selection": MultiLabelQuestion,
    "ranking": RankingQuestion,
    "text": TextQuestion,
    "rating": RatingQuestion,
    "span": SpanQuestion,
}


def question_from_model(model: QuestionModel) -> QuestionType:
    try:
        return _TYPE_TO_CLASS[model.settings.type].from_model(model)
    except KeyError:
        raise ValueError(f"Unsupported question model type: {model.settings.type}")
