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

from argilla_sdk._resource import Resource
from argilla_sdk._models import DatasetModel
from argilla_sdk.settings import Settings


__all__ = ["Dataset"]


class Dataset(Resource):
    def __init__(
        self,
        settings: Settings = Settings(),
        **kwargs,
    ) -> None:
        self._model = DatasetModel(**kwargs)
        self.__define_settings(settings=settings)

    def __define_settings(
        self,
        settings: Settings,
    ) -> None:
        """ Populate the dataset object with settings"""
        self._settings = settings
        self.guidelines = settings.guidelines
        self.fields = settings.fields
        self.questions = settings.questions
        self.allow_extra_metadata = settings.allow_extra_metadata
