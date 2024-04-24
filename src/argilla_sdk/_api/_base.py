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

import json
from datetime import datetime
from requests.exceptions import HTTPError
from requests.models import Response
from typing import Generic, TYPE_CHECKING, TypeVar, Union
from uuid import UUID

from argilla_sdk._exceptions import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    UnprocessableEntityError,
    InternalServerError,
)
from argilla_sdk._helpers._mixins import LoggingMixin
from argilla_sdk._models import ResourceModel


if TYPE_CHECKING:
    from httpx import Client


__all__ = ["ResourceAPI"]

T = TypeVar("T")


# TODO: Use ABC and align all the abstract method for the different resources APIs
# See comment https://github.com/argilla-io/argilla-python/pull/33#discussion_r1532079989
class ResourceAPI(LoggingMixin, Generic[T]):
    """Base class for all API resources that contains common methods."""

    def __init__(self, http_client: "Client") -> None:
        self.http_client = http_client

    ################
    # CRUD methods #
    ################

    def get(self, id: UUID) -> T:
        raise NotImplementedError

    def create(self, resource: T) -> T:
        raise NotImplementedError

    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    def update(self, resource: T) -> T:
        return resource

    ####################
    # Utility methods #
    ####################

    def _date_from_iso_format(self, date: str) -> datetime:
        return datetime.fromisoformat(date)

    def _handle_response(self, response: Response, resource: Union[ResourceModel, UUID]):
        """Handle the response from the API and raise exceptions if necessary."""
        try:
            data = response.json()
        except ValueError:
            data = None

        if 200 <= response.status_code < 300:
            return data

        if response.status_code == 400:
            raise BadRequestError(f"Bad Request: request = {resource} response = {data}")
        elif response.status_code == 403:
            raise ForbiddenError(f"Forbidden: request = {resource} response = {data}")
        elif response.status_code == 404:
            raise NotFoundError(f"Not Found: request = {resource} response = {data}")
        elif response.status_code == 409:
            raise ConflictError(f"Conflict: request = {resource} response = {data}")
        elif response.status_code == 422:
            raise UnprocessableEntityError(f"Unprocessable Entity: request = {resource} response = {data}")
        elif response.status_code == 500:
            raise InternalServerError(f"Internal Server Error: request = {resource} response = {data}")

        raise HTTPError(f"HTTP {response.status_code} Error: request = {resource} response = {data}", response=response)

    def _parse_error(self, response) -> str:
        error_details = response.json()
        return f"{error_details.get('detail', {}).get('code')}: {json.dumps(error_details.get('detail', {}).get('params', {}))}"
