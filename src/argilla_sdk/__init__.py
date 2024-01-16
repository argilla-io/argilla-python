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

from argilla_sdk._api import HTTPClientConfig, create_http_client  # noqa
from argilla_sdk.workspaces import *  # noqa

DEFAULT_HTTP_CLIENT: Optional[httpx.Client] = None
DEFAULT_HTTP_CONFIG = HTTPClientConfig(api_url=os.getenv("ARGILLA_API_URL"), api_key=os.getenv("ARGILLA_API_KEY"))


def init(
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 60,
    **client_args,
) -> None:
    """Initialize the SDK with the given API URL and API key."""

    global DEFAULT_HTTP_CLIENT
    global DEFAULT_HTTP_CONFIG

    api_url = api_url or DEFAULT_HTTP_CONFIG.api_url
    api_key = api_key or DEFAULT_HTTP_CONFIG.api_key

    DEFAULT_HTTP_CLIENT = create_http_client(api_url, api_key, timeout, **client_args)


def get_default_http_client() -> httpx.Client:
    """Get the default HTTP client."""
    global DEFAULT_HTTP_CLIENT

    if DEFAULT_HTTP_CLIENT is None:
        raise RuntimeError("SDK not initialized. Call argilla_sdk.init() first.")

    return DEFAULT_HTTP_CLIENT
