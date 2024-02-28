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

from argilla_sdk._helpers._log import log


class LoggingMixin:
    """A utility mixin for logging."""

    def log(self, message: str, level: str = "info") -> None:
        class_name = self.__class__.__name__
        message = f"{class_name}: {message}"
        log(level=level, message=message)
