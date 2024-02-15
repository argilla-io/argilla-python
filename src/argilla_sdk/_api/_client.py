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

import os
from typing import Optional

import httpx

from argilla_sdk._api import HTTPClientConfig, create_http_client
from argilla_sdk._api._workspaces import WorkspacesAPI
from argilla_sdk._api._users import UsersAPI
from argilla_sdk._api._datasets import DatasetsAPI

__all__ = ["APIClient"]


DEFAULT_ARGILLA_API_URL = os.getenv("ARGILLA_API_URL")
DEFAULT_ARGILLA_API_KEY = os.getenv("ARGILLA_API_KEY")
DEFAULT_WORKSPACE_NAME = os.getenv("ARGILLA_WORKSPACE_NAME", "admin")
DEFAULT_USERNAME = os.getenv("ARGILLA_USERNAME", "admin")
DEFAULT_HTTP_CONFIG = HTTPClientConfig(api_url=DEFAULT_ARGILLA_API_URL, api_key=DEFAULT_ARGILLA_API_KEY)


class APIClient:
    """Initialize the SDK with the given API URL and API key."""

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
        return create_http_client(self.api_url, self.api_key, self.timeout)

    @property
    def workspaces(self) -> "WorkspacesAPI":
        return WorkspacesAPI(self.http_client)

    @property
    def users(self) -> "User":
        return UsersAPI(self.http_client)

    @property
    def datasets(self) -> "Dataset":
        return DatasetsAPI(self.http_client)
