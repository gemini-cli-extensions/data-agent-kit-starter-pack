# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrapper model for union of v1 and v2 pipeline models."""

from typing import Literal, Union

from declarative_dags_models.v1.pipeline_model import PipelineModel as PipelineModelV1
from declarative_dags_models.v2.pipeline_model import PipelineModel as PipelineModelV2
from pydantic import Field
from typing_extensions import Annotated


class V1Model(PipelineModelV1):
  model_version: Literal['v1']


class V2Model(PipelineModelV2):
  model_version: Literal['v2']


DeclarativeDagsModel = Annotated[
    Union[V1Model, V2Model], Field(discriminator='model_version')
]
