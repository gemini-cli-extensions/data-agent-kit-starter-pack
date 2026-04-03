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
from datetime import datetime
from typing import Literal, Optional
from croniter import croniter
from pydantic import BaseModel, field_validator, model_validator
import pytz


class ScheduleTriggerModel(BaseModel):
  type: Literal['schedule']
  scheduleInterval: str
  startTime: str
  endTime: str
  catchup: bool
  timezone: Optional[str] = 'UTC'

  @field_validator('scheduleInterval')
  @classmethod
  def validate_cron_expression(cls, v: str) -> str:
    if not croniter.is_valid(v):
      raise ValueError(f'Invalid CRON expression: {v}')
    return v

  @field_validator('timezone')
  @classmethod
  def validate_timezone(cls, v: str) -> str:
    try:
      pytz.timezone(v)
      return v
    except:
      raise ValueError(f'Invalid timezone: {v}')

  @model_validator(mode='after')
  def check_start_end_times(self):
    parsedStartTime = datetime.fromisoformat(self.startTime)
    parsedEndTime = datetime.fromisoformat(self.endTime)
    if parsedEndTime < parsedStartTime:
      raise ValueError('endTime must be after startTime')
    return self
