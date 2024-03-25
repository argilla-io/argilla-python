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

import logging
import os
from typing import Optional

import httpx

from argilla_sdk._api import HTTPClientConfig, create_http_client
from argilla_sdk._api._datasets import DatasetsAPI
from argilla_sdk._api._fields import FieldsAPI
from argilla_sdk._api._questions import QuestionsAPI
from argilla_sdk._api._records import RecordsAPI
from argilla_sdk._api._users import UsersAPI
from argilla_sdk._api._workspaces import WorkspacesAPI
from argilla_sdk._constants import _DEFAULT_API_KEY, _DEFAULT_API_URL

__all__ = ["APIClient"]


ARGILLA_API_URL = os.getenv(key="ARGILLA_API_URL", default=_DEFAULT_API_URL)
ARGILLA_API_KEY = os.getenv(key="ARGILLA_API_KEY", default=_DEFAULT_API_KEY)
DEFAULT_HTTP_CONFIG = HTTPClientConfig(api_url=ARGILLA_API_URL, api_key=ARGILLA_API_KEY)


class ArgillaAPI:
    """Argilla API access object."""

    def __init__(self, http_client: httpx.Client):
        self.http_client = http_client

        self.__workspaces = WorkspacesAPI(http_client=self.http_client)
        self.__datasets = DatasetsAPI(http_client=self.http_client)
        self.__users = UsersAPI(http_client=self.http_client)
        self.__fields = FieldsAPI(http_client=self.http_client)
        self.__questions = QuestionsAPI(http_client=self.http_client)
        self.__records = RecordsAPI(http_client=self.http_client)

    @property
    def workspaces(self) -> "WorkspacesAPI":
        return self.__workspaces

    @property
    def users(self) -> "UsersAPI":
        return self.__users

    @property
    def datasets(self) -> "DatasetsAPI":
        return self.__datasets

    @property
    def fields(self) -> "FieldsAPI":
        return self.__fields

    @property
    def questions(self) -> "QuestionsAPI":
        return self.__questions

    @property
    def records(self) -> "RecordsAPI":
        return self.__records


class APIClient:
    """Initialize the SDK with the given API URL and API key.
    This class is used to create an instance of the Argilla API client.
    """

    def __init__(
        self,
        api_url: Optional[str] = DEFAULT_HTTP_CONFIG.api_url,
        api_key: Optional[str] = DEFAULT_HTTP_CONFIG.api_key,
        timeout: int = 60,
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.timeout = timeout

    @property
    def http_client(self) -> httpx.Client:
        return create_http_client(
            api_url=self.api_url,  # type: ignore
            api_key=self.api_key,  # type: ignore
            timeout=self.timeout,
        )

    @property
    def api(self) -> "ArgillaAPI":
        return ArgillaAPI(http_client=self.http_client)

    ##############################
    # Utility methods
    ##############################

    def log(self, message: str, level: int = logging.INFO) -> None:
        class_name = self.__class__.__name__
        message = f"{class_name}: {message}"
        logging.log(level=level, msg=message)
