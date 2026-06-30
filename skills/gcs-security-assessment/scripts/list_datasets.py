# Copyright 2026 Google LLC
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

"""Script to list Storage Insights datasets.

This script lists all DatasetConfigs within a specified GCP project and location
using the Storage Insights API.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, MutableSequence, Sequence
import json
from typing import Any

# pylint: disable=g-import-not-at-top
try:
  from google3.third_party.data_agent_kit.data_agent_common.skills.gcs_security_assessment.scripts import cloud_rest_helpers_nodeps
except ImportError:
  import cloud_rest_helpers_nodeps  # type: ignore
# pylint: enable=g-import-not-at-top

_TIMEOUT_SECONDS = 10
_SKILL = "gcs-security-assessment"
_SCRIPT = "list-datasets"


def list_datasets(
    *,
    project_id: str,
    location: str,
    session: Any,
) -> Sequence[Mapping[str, str]]:
  """Lists Storage Insights linked datasets using public HTTP REST endpoint.

  Args:
    project_id: The GCP project ID.
    location: The dataset location.
    session: The authorized session to make requests.

  Returns:
    A list of dictionaries mapping {"{LOCATION_NAME}": "{DATASET_ID}",
    "description":
    "{DESCRIPTION}"} where each field is extracted from the SI dataset.

  Raises:
    RuntimeError: If the request fails.
  """
  url = f"https://storageinsights.googleapis.com/v1/projects/{project_id}/locations/{location}/datasetConfigs"
  try:
    response = session.get(url, timeout=_TIMEOUT_SECONDS)
    response.raise_for_status()
  except cloud_rest_helpers_nodeps.CloudRestError as e:
    raise RuntimeError(
        f"Failed to fetch dataset configs for '{location}':'{project_id}' with"
        f" error: {e!r}"
    ) from e
  else:
    data = response.json()
  configs = data.get("datasetConfigs") or []
  result: MutableSequence[Mapping[str, str]] = []
  for config in configs:
    name = config.get("name") or ""
    link = config.get("link") or {}
    description = config.get("description") or ""
    if link.get("linked") and link.get("dataset") and "/locations/" in name:
      _, location_path = name.split("/locations/")
      loc, *_ = location_path.split("/")
      result.append({loc: str(link.get("dataset")), "description": description})
  return result


def main() -> None:
  parser = argparse.ArgumentParser(
      description="List Storage Insights datasets for a project and location."
  )
  parser.add_argument(
      "--project_id", type=str, required=True, help="The GCP project ID."
  )
  parser.add_argument(
      "--location", type=str, default="-", help="The dataset location."
  )
  args = parser.parse_args()

  try:
    with cloud_rest_helpers_nodeps.get_authorized_session(
        skill=_SKILL, script=_SCRIPT, project_id=args.project_id
    ) as session:
      datasets = list_datasets(
          project_id=args.project_id,
          location=args.location,
          session=session,
      )
      print(json.dumps(datasets, indent=2))
  except (
      cloud_rest_helpers_nodeps.CredentialsError,
      RuntimeError,
  ) as e:
    print(json.dumps({"error": repr(e)}))


if __name__ == "__main__":
  main()
