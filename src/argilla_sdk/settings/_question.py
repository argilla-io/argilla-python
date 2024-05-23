# Copyright 2024-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional, Union

from argilla_sdk._models._settings._questions import (
    LabelQuestionModel,
    LabelQuestionSettings,
    MultiLabelQuestionModel,
    RankingQuestionModel,
    TextQuestionModel,
    TextQuestionSettings,
    RatingQuestionModel,
    QuestionModel,
    SpanQuestionSettings,
    SpanQuestionModel,
    RatingQuestionSettings,
    MultiLabelQuestionSettings,
    RankingQuestionSettings,
)
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
        visible_labels: Optional[int] = None,
    ) -> None:
        """ Define a new label question for `Settings` of a `Dataset`. A label \
            question is a question where the user can select one label from \
            a list of available labels.
        
        Parameters:
            name: str: The name of the question to be used as a reference.
            labels: List[str]: The list of available labels for the question.
            title: Optional[str]: The title of the question to be shown in the UI.
            description: Optional[str]: The description of the question to be shown in the UI.
            required: bool: If the question is required for a record to be valid.
            visible_labels: Optional[int]: The number of visible labels for the question.
        """
        self._model = LabelQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            settings=LabelQuestionSettings(
                options=self._render_values_as_options(labels), visible_options=visible_labels
            ),
        )

    @classmethod
    def from_model(cls, model: LabelQuestionModel) -> "LabelQuestion":
        instance = cls(name=model.name, labels=cls._render_options_as_values(model.settings.options))
        instance._model = model
        return instance

    ##############################
    # Public properties
    ##############################

    @property
    def labels(self) -> List[str]:
        return self._render_options_as_labels(self._model.settings.options)

    @labels.setter
    def labels(self, labels: List[str]) -> None:
        self._model.settings.options = self._render_values_as_options(labels)

    @property
    def visible_labels(self) -> Optional[int]:
        return self._model.settings.visible_options

    @visible_labels.setter
    def visible_labels(self, visible_labels: Optional[int]) -> None:
        self._model.settings.visible_options = visible_labels

    ##############################
    # Private methods
    ##############################


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
        """Create a new multilabel question for `Settings` of a `Dataset`. A \
            multilabel question is a question where the user can select multiple \
            labels from a list of available labels.
            
        Parameters:
            name: str: The name of the question to be used as a reference.
            labels: List[str]: The list of available labels for the question.
            title: Optional[str]: The title of the question to be shown in the UI.
            description: Optional[str]: The description of the question to be shown in the UI.
            required: bool: If the question is required for a record to be valid.
            visible_labels: Optional[int]: The number of visible labels for the question.
        """
        self._model = MultiLabelQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            settings=MultiLabelQuestionSettings(
                options=self._render_values_as_options(labels), visible_options=visible_labels
            ),
        )

    @classmethod
    def from_model(cls, model: MultiLabelQuestionModel) -> "MultiLabelQuestion":
        instance = cls(name=model.name, labels=cls._render_options_as_values(model.settings.options))
        instance._model = model

        return instance


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
        """Create a new text question for `Settings` of a `Dataset`. A text question \
            is a question where the user can input text.
            
        Parameters:
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
            settings=TextQuestionSettings(use_markdown=use_markdown),
        )

    @classmethod
    def from_model(cls, model: TextQuestionModel) -> "TextQuestion":
        instance = cls(name=model.name)
        instance._model = model

        return instance

    @property
    def use_markdown(self) -> bool:
        return self._model.settings.use_markdown

    @use_markdown.setter
    def use_markdown(self, use_markdown: bool) -> None:
        self._model.settings.use_markdown = use_markdown


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
        """Create a new rating question for `Settings` of a `Dataset`. A rating question \
            is a question where the user can select a value from a sequential list of options.
            
        Parameters:
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
            settings=RatingQuestionSettings(options=self._render_values_as_options(values)),
        )

    @classmethod
    def from_model(cls, model: RatingQuestionModel) -> "RatingQuestion":
        instance = cls(name=model.name, values=cls._render_options_as_values(model.settings.options))
        instance._model = model

        return instance

    @property
    def values(self) -> List[int]:
        return self._render_options_as_labels(self._model.settings.options)

    @values.setter
    def values(self, values: List[int]) -> None:
        self._model.values = self._render_values_as_options(values)


class RankingQuestion(SettingsPropertyBase):
    _model: RankingQuestionModel

    def __init__(
        self,
        name: str,
        values: List[str],
        title: Optional[str] = None,
        description: Optional[str] = None,
        required: bool = True,
    ) -> None:
        """Create a new ranking question for `Settings` of a `Dataset`. A ranking question \
            is a question where the user can rank a list of options.
        
        Parameters:
            name: str: The name of the question to be used as a reference.
            values: List[str]: The list of available values for the question.
            title: Optional[str]: The title of the question to be shown in the UI.
            description: Optional[str]: The description of the question to be shown in the UI.
            required: bool: If the question is required for a record to be valid.
        """
        self._model = RankingQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            settings=RankingQuestionSettings(options=self._render_values_as_options(values)),
        )

    @classmethod
    def from_model(cls, model: RankingQuestionModel) -> "RankingQuestion":
        instance = cls(name=model.name, values=cls._render_options_as_values(model.settings.options))
        instance._model = model

        return instance

    @property
    def values(self) -> List[str]:
        return self._render_options_as_labels(self._model.settings.options)

    @values.setter
    def values(self, values: List[int]) -> None:
        self._model.settings.options = self._render_values_as_options(values)


class SpanQuestion(SettingsPropertyBase):
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
        """ Create a new span question for `Settings` of a `Dataset`. A span question \
            is a question where the user can select a section of text within a text field \
            and assign it a label.
            
            Parameters:
                name: str: The name of the question to be used as a reference.
                field: str: The name of the text field to apply the span question to.
                labels: List[str]: The list of available labels for the question.
                allow_overlapping: bool: If the user can select overlapping spans.
                visible_labels: Optional[int]: The number of labels to show at once.
                title: Optional[str]: The title of the question to be shown in the UI.
                description: Optional[str]: The description of the question to be shown in the UI.
                required: bool: If the question is required for a record to be valid.
            """
        self._model = SpanQuestionModel(
            name=name,
            title=title,
            description=description,
            required=required,
            settings=SpanQuestionSettings(
                field=field,
                allow_overlapping=allow_overlapping,
                visible_options=visible_labels,
                options=self._render_values_as_options(labels),
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
        return self._render_options_as_labels(self._model.settings.options)

    @labels.setter
    def labels(self, labels: List[str]) -> None:
        self._model.settings.options = self._render_values_as_options(labels)

    @classmethod
    def from_model(cls, model: SpanQuestionModel) -> "SpanQuestion":
        instance = cls(
            name=model.name,
            field=model.settings.field,
            labels=cls._render_options_as_values(model.settings.options),
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
