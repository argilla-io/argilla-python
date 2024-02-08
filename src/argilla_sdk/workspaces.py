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

from typing import TYPE_CHECKING

from argilla_sdk import _api
from argilla_sdk._helpers import GenericIterator  # noqa

if TYPE_CHECKING:
    from argilla_sdk.datasets import WorkspaceDatasets

if TYPE_CHECKING:
    from argilla_sdk.datasets import WorkspaceDatasets
    from argilla_sdk.users import WorkspaceUsers

__all__ = ["Workspace"]


class Workspace(_api.Workspace):
    @property
    def datasets(self) -> "WorkspaceDatasets":
        from argilla_sdk.datasets import WorkspaceDatasets

        return WorkspaceDatasets(self)

    @property
    def users(self) -> "WorkspaceUsers":
        from argilla_sdk.users import WorkspaceUsers

        return WorkspaceUsers(self)
