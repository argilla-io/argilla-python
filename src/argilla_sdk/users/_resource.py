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

from typing import Optional
from uuid import UUID

from argilla_sdk._api import UsersAPI
from argilla_sdk.client import Argilla
from argilla_sdk._resource import Resource
from argilla_sdk._models import UserModel, Role


class User(Resource):
    """Class for interacting with Argilla users in the Argilla server. User profiles \
        are used to manage access to the Argilla server and track responses to records.
        
    Attributes:
        username (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        role (str): The role of the user, either 'annotator' or 'admin'.
        password (str): The password of the user.
        id (UUID): The ID of the user.
    """

    _model: UserModel
    _api: UsersAPI

    def __init__(
        self,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        role: Optional[str] = None,
        password: Optional[str] = None,
        client: Optional["Argilla"] = Argilla(),
        id: Optional[UUID] = None,
        _model: Optional[UserModel] = None,
    ) -> None:
        """Initializes a User object with a client and a username

        Parameters:
            client (Argilla): The client used to interact with Argilla
            username (str): The username of the user
            first_name (str): The first name of the user
            last_name (str): The last name of the user
            role (str): The role of the user, either 'annotator', admin, or 'owner'
            password (str): The password of the user

        Returns:
            User: The initialized user object
        ```
        """
        super().__init__(
            client=client,
            api=client.api.users,
        )
        if _model is None:
            _model = UserModel(
                username=username,
                first_name=first_name or username,
                last_name=last_name or username,
                role=role or Role.annotator,
                password=password,
                id=id,
            )
            self.log(f"Initialized user with username {username}")
        self._sync(model=_model)
