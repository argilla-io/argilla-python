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
import logging

import httpx

__all__ = ["ResourceAPI"]


class ResourceAPI:
    """Base class for all API resources that contains common methods."""

    logger = logging.getLogger(name="argilla_sdk.api.resources")

    def __init__(self, http_client: httpx.Client) -> None:
        self.http_client = http_client

    def _date_from_iso_format(self, date: str) -> datetime:
        return datetime.fromisoformat(date)

    def log(self, message: str, level: str = "info") -> None:
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        level_int = level_map.get(level, logging.INFO)
        class_name = self.__class__.__name__
        message = f"{class_name}: {message}"
        self.logger.log(level=level_int, msg=message)
