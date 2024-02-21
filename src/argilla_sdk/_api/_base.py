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

from datetime import datetime
from typing import TYPE_CHECKING

from argilla_sdk._helpers._mixins import LoggingMixin


if TYPE_CHECKING:
    from httpx import Client


__all__ = ["ResourceAPI"]


class ResourceAPI(LoggingMixin):
    """Base class for all API resources that contains common methods."""

    def __init__(self, http_client: "Client") -> None:
        self.http_client = http_client

    def _date_from_iso_format(self, date: str) -> datetime:
        return datetime.fromisoformat(date)