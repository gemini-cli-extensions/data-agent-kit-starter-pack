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
from enum import Enum
from typing import List, Optional, Union
from declarative_dags_models.v1.action_models import BqOperationActionModel, DBTActionModel, NotebookOperatorActionModel, PythonScriptActionModel, PythonVirtualenvActionModel
from declarative_dags_models.v1.trigger_models import ScheduleTriggerModel
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated

# Define a Union of all possible action models for this version.
# In the future, if you add a NewActionModel, just add it to this Union.
# e.g., AnyAction = Union[PapermillActionModel, NewActionModel]
AnyAction = Union[
    PythonScriptActionModel,
    PythonVirtualenvActionModel,
    NotebookOperatorActionModel,
    BqOperationActionModel,
    DBTActionModel,
]
AnyScheduleTrigger = Union[ScheduleTriggerModel]


class RunnerType(str, Enum):
  CORE = 'core'
  AIRFLOW = 'airflow'


class ExecutionConfigModel(BaseModel):
  retries: int = Field(ge=1)


class DefaultsModel(BaseModel):
  project: str
  region: str
  executionConfig: ExecutionConfigModel


class PipelineModel(BaseModel):
  pipelineId: str = Field(pattern=r'^[a-zA-Z0-9_.-]+$')
  description: str
  runner: RunnerType
  owner: str
  tags: Optional[List[str]] = None
  defaults: DefaultsModel
  triggers: List[Annotated[AnyScheduleTrigger, Field(discriminator='type')]]
  actions: List[Annotated[AnyAction, Field(discriminator='type')]]
  airflow_version: str

  @classmethod
  def build(cls, definition: dict):
    try:
      return cls.model_validate(definition)
    except ValidationError:
      raise
