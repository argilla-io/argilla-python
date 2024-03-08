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


from typing import List, Optional, Union, TYPE_CHECKING

from argilla_sdk._models._resource import ResourceModel

if TYPE_CHECKING:
    from argilla_sdk._models import (
        TextField,
        LabelQuestion,
        MultiLabelQuestion,
        RankingQuestion,
        TextQuestion,
        RatingQuestion,
    )


class SettingsModel(ResourceModel):
    fields: Optional[List["TextField"]] = []
    questions: Optional[
        List[
            Union[
                "LabelQuestion",
                "MultiLabelQuestion",
                "RankingQuestion",
                "TextQuestion",
                "RatingQuestion",
            ]
        ]
    ] = []
    guidelines: Optional[str] = None
    allow_extra_metadata: Optional[bool] = False

    class Config:
        validate_assignment = True
