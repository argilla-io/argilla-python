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
from typing import Union, Optional

from argilla_sdk._resource import Resource
from argilla_sdk._models import DatasetModel
from argilla_sdk.settings import Settings
from argilla_sdk.settings.fields import FieldBase
from argilla_sdk.settings.questions import QuestionBase


__all__ = ["Dataset"]


class Dataset(Resource):
    def __init__(
        self,
        settings: Settings = Settings(),
        guidelines: Union[str, None] = None,
        fields: Optional[list[FieldBase]] = None,
        questions: Optional[list[QuestionBase]] = None,
        **kwargs,
    ) -> None:
        self._model = DatasetModel(**kwargs)
        self.__define_settings(settings=settings, guidelines=guidelines, fields=fields, questions=questions)

    def __define_settings(
        self,
        settings: Settings,
        guidelines: Union[str, None] = None,
        fields: Optional[list[FieldBase]] = None,
        questions: Optional[list[QuestionBase]] = None,
    ) -> None:
        self.guidelines = guidelines or settings.guidelines
        self.fields = fields or settings.fields
        self.questions = questions or settings.questions
