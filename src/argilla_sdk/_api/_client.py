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
from dataclasses import dataclass, field
from typing import List, Optional

import httpx

from argilla_sdk._api import HTTPClientConfig, create_http_client
from argilla_sdk._api._workspaces import Workspace
from argilla_sdk._api._users import User
from argilla_sdk._api._datasets import Dataset

__all__ = ["Client"]


DEFAULT_ARGILLA_API_URL = os.getenv("ARGILLA_API_URL")
DEFAULT_ARGILLA_API_KEY = os.getenv("ARGILLA_API_KEY")
DEFAULT_WORKSPACE_NAME = os.getenv("ARGILLA_WORKSPACE_NAME", "admin")
DEFAULT_USERNAME = os.getenv("ARGILLA_USERNAME", "admin")
DEFAULT_HTTP_CONFIG = HTTPClientConfig(api_url=DEFAULT_ARGILLA_API_URL, api_key=DEFAULT_ARGILLA_API_KEY)


@dataclass
class Client:
    """Initialize the SDK with the given API URL and API key."""

    api_url: Optional[str] = DEFAULT_HTTP_CONFIG.api_url
    api_key: Optional[str] = DEFAULT_HTTP_CONFIG.api_key
    timeout: int = 60

    @property
    def http_client(self) -> httpx.Client:
        return create_http_client(self.api_url, self.api_key, self.timeout)

    @property
    def workspaces(self) -> "Workspace":
        return Workspace(self.http_client)

    @property
    def users(self) -> "User":
        return User
