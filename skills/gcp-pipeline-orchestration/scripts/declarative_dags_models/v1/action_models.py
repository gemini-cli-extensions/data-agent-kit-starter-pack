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
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, model_validator


class ActionBaseModel(BaseModel):
  name: str
  dependsOn: Optional[List[str]] = None


class PythonScriptConfigurationModel(BaseModel):
  pythonCallable: str
  opKwargs: Optional[Dict[str, Any]] = None


class PythonScriptActionModel(ActionBaseModel):
  type: Literal['script']
  filename: str
  config: PythonScriptConfigurationModel


class PythonVirtualenvConfigurationModel(PythonScriptConfigurationModel):
  requirementsPath: Optional[str] = None
  requirements: Optional[List[str]] = None
  systemSitePackages: Optional[bool] = None

  @model_validator(mode='after')
  def check_requirements_or_path(self):
    if (
        bool(self.requirements) == bool(self.requirementsPath)
        and self.requirements
    ):
      raise ValueError(
          'Either "requirements" list or "requirementsPath" must be provided,'
          ' but not both.'
      )
    return self


class PythonVirtualenvActionModel(ActionBaseModel):
  type: Literal['python-virtual-env']
  filename: str
  config: PythonVirtualenvConfigurationModel


class SessionTemplateModel(BaseModel):
  inline: Optional[Dict[str, Any]] = None
  gcsReference: Optional[str] = None
  name: Optional[str] = None

  @model_validator(mode='after')
  def check_exclusive_fields(self):
    if (
        sum([
            self.inline is not None,
            self.gcsReference is not None,
            self.name is not None,
        ])
        != 1
    ):
      raise ValueError(
          'Exactly one of "inline", "gcsReference", or "name" must be provided.'
      )
    return self


class DataprocCreateBatchOperatorConfigurationModel(BaseModel):
  sessionTemplate: SessionTemplateModel


class BqOperationConfigurationModel(BaseModel):
  location: str
  destinationTable: Optional[str] = None


class BqOperationActionModel(ActionBaseModel):
  type: Literal['operation']
  engine: Literal['bq']
  query: Optional[str] = None
  filename: Optional[str] = None
  config: BqOperationConfigurationModel

  @model_validator(mode='after')
  def check_query_or_filename(self):
    if bool(self.query) == bool(self.filename):
      raise ValueError(
          'Either "query" or "filename" must be provided, but not both.'
      )
    return self


class DataprocEphemeralConfigurationModel(BaseModel):
  region: str
  project_id: str
  cluster_name: str
  cluster_config: Dict[str, Any]
  job: Dict[str, Any]


class DataprocGceExistingClusterConfigurationModel(BaseModel):
  cluster: str


class EngineModel(BaseModel):
  engineType: Literal['dataproc-gce', 'dataproc-serverless']
  clusterMode: Optional[Literal['existing', 'ephemeral']] = None


class NotebookOperatorActionModel(ActionBaseModel):
  type: Literal['notebook', 'dataproc-script']
  filename: str
  executionTimeout: Optional[str] = None
  region: str
  engine: EngineModel
  archives: Optional[List[str]] = None
  depsBucket: Optional[str] = None
  config: Union[
      DataprocGceExistingClusterConfigurationModel,
      DataprocEphemeralConfigurationModel,
      DataprocCreateBatchOperatorConfigurationModel,
      None,
  ] = None

  @model_validator(mode='after')
  def check_engine_config(self):
    engine = self.engine
    config = self.config
    if engine:
      if engine.engineType == 'dataproc-gce':
        if not engine.clusterMode:
          raise ValueError("clusterMode is required for 'dataproc-gce' engine")
        if not config:
          raise ValueError("config is required for 'dataproc-gce' engine")
        if engine.clusterMode == 'existing':
          if not isinstance(
              config, DataprocGceExistingClusterConfigurationModel
          ):
            raise ValueError('Incorrect config type for existing cluster')
        elif engine.clusterMode == 'ephemeral':
          if not isinstance(config, DataprocEphemeralConfigurationModel):
            raise ValueError('Incorrect config type for ephemeral cluster')

      elif engine.engineType == 'dataproc-serverless':
        if engine.clusterMode:
          raise ValueError(
              "clusterMode is not allowed for 'dataproc-serverless' engine"
          )
        if not config:
          raise ValueError(
              "config is required for 'dataproc-serverless' engine"
          )
        if not isinstance(
            config, DataprocCreateBatchOperatorConfigurationModel
        ):
          raise ValueError('Incorrect config type for dataproc-serverless')
    return self


class DbtLocalExecutionModel(BaseModel):
  path: str


class DBTActionModel(ActionBaseModel):
  type: Literal['pipeline']
  engine: Literal['dbt']
  executionMode: Literal['local']
  source: DbtLocalExecutionModel
  select_models: Optional[List[str]] = None


AllActions = Union[
    PythonScriptActionModel,
    PythonVirtualenvActionModel,
    BqOperationActionModel,
    NotebookOperatorActionModel,
    DBTActionModel,
]
