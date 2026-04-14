#!/usr/bin/env python3
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
"""BigQuery Data Transfer Service REST API - Data Source Parameter Discovery."""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request


def get_project_id():
  """Retrieves the active Google Cloud project ID from the environment or CLI."""
  project_id = os.environ.get("PROJECT_ID")
  if project_id:
    return project_id
  try:
    result = subprocess.run(
        ["gcloud", "config", "get-value", "project"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
  except subprocess.CalledProcessError:
    print("Error: Could not determine PROJECT_ID.", file=sys.stderr)
    sys.exit(1)
  except FileNotFoundError:
    try:
      result = subprocess.run(
          ["gcloud.cmd", "config", "get-value", "project"],
          capture_output=True,
          text=True,
          check=True,
      )
      return result.stdout.strip()
    except Exception:  # pylint: disable=broad-exception-caught
      print("Error: gcloud command not found.", file=sys.stderr)
      sys.exit(1)


def get_token():
  """Retrieves the access token using the gcloud CLI."""
  try:
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
  except FileNotFoundError:
    try:
      result = subprocess.run(
          ["gcloud.cmd", "auth", "print-access-token"],
          capture_output=True,
          text=True,
          check=True,
      )
      return result.stdout.strip()
    except Exception:  # pylint: disable=broad-exception-caught
      print("Error: gcloud command not found.", file=sys.stderr)
      sys.exit(1)
  except subprocess.CalledProcessError:
    print(
        "Error: Could not obtain access token. Are you logged in?",
        file=sys.stderr,
    )
    sys.exit(1)


def main():
  """Main entry point for the script."""
  parser = argparse.ArgumentParser(
      description=(
          "BigQuery Data Transfer Service REST API - "
          "Data Source Parameter Discovery"
      )
  )
  parser.add_argument("--project_id", help="The GCP project ID to use")
  parser.add_argument("data_source_id", help="The DATA_SOURCE_ID to inspect")
  parser.add_argument(
      "region", nargs="?", default="us", help="The GCP region (default: us)"
  )
  args = parser.parse_args()

  project_id = args.project_id or get_project_id()
  if not project_id:
    print(
        "Error: PROJECT_ID not set and could not be determined.",
        file=sys.stderr,
    )
    sys.exit(1)

  print(
      f"Retrieving Data Source parameters for: {args.data_source_id} "
      f"in {args.region}..."
  )

  base_url = (
      "https://bigquerydatatransfer.googleapis.com/v1/"
      f"projects/{project_id}/locations/{args.region}"
  )
  url = f"{base_url}/dataSources/{args.data_source_id}"

  token = get_token()

  req = urllib.request.Request(url)
  req.add_header("Authorization", f"Bearer {token}")
  req.add_header("Content-Type", "application/json")

  try:
    with urllib.request.urlopen(req) as response:
      data = json.loads(response.read().decode("utf-8"))
      print(json.dumps(data, indent=4))
  except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
    print(e.read().decode("utf-8"), file=sys.stderr)
    sys.exit(1)
  except Exception as e:  # pylint: disable=broad-exception-caught
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  main()
