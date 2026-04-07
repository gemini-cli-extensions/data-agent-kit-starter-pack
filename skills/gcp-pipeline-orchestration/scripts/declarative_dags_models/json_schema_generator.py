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
"""Generates a JSON schema from the DeclarativeDagsModel."""

import importlib
import inspect
import json
import os
from pathlib import Path
import sys
from pydantic import TypeAdapter

# The full import path to the file where DeclarativeDagsModel is defined
MODEL_MODULE_PATH = "declarative_dags_models.declarative_dags_model"
TARGET_MODEL_NAME = "DeclarativeDagsModel"


def generate_schema():
  """Imports the model module and saves JSON schema

  inside that module's directory.
  """
  # Ensure current working directory is in sys.path for GitHub Action imports
  cwd = os.getcwd()
  if cwd not in sys.path:
    sys.path.insert(0, cwd)

  print(
      f"🔍 Attempting to import {TARGET_MODEL_NAME} from {MODEL_MODULE_PATH}."
  )

  try:
    # 1. Import the module
    module = importlib.import_module(MODEL_MODULE_PATH)

    # 2. Get the physical path of that module
    module_file = inspect.getfile(module)
    module_dir = Path(module_file).parent

    # 3. Grab the DeclarativeDagsModel attribute
    if hasattr(module, TARGET_MODEL_NAME):
      obj = getattr(module, TARGET_MODEL_NAME)

      # 4. Use TypeAdapter to handle the Annotated Union
      adapter = TypeAdapter(obj)
      schema_dict = adapter.json_schema()

      # 5. Add metadata for VS Code
      schema_dict["$schema"] = "https://json-schema.org/draft/2020-12/schema"
      schema_dict["title"] = TARGET_MODEL_NAME

      # 6. Define output path
      output_dir = module_dir / "schemas"
      output_dir.mkdir(parents=True, exist_ok=True)
      output_file = output_dir / "declarative_dags_model_schema.json"

      with open(output_file, "w", encoding="utf-8") as f:
        # Added sort_keys=True to keep GitHub diffs clean
        json.dump(schema_dict, f, indent=2, sort_keys=True)

      print("✅ Success!")
      print(f"📂 Module Path: {module_dir}")
      print(f"💾 Schema saved to: {output_file.absolute()}")
    else:
      print(f"❌ Error: {TARGET_MODEL_NAME} not found in {MODEL_MODULE_PATH}")
      sys.exit(1)  # Signal failure to GitHub Action

  except ImportError as e:
    print(f"❌ Critical Error: Could not import {MODEL_MODULE_PATH}. {e}")
    sys.exit(1)
  except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
    sys.exit(1)


if __name__ == "__main__":
  generate_schema()
