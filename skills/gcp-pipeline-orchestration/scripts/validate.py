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
"""Defines the CLI for the Declarative DAGs."""

from pathlib import Path
import click
from declarative_dags_models.v1.pipeline_model import PipelineModel as v1_pipeline_model
from declarative_dags_models.v2.pipeline_model import PipelineModel as v2_pipeline_model
from pydantic import ValidationError
import yaml

MODEL_MAP = {"v1": v1_pipeline_model, "v2": v2_pipeline_model}


@click.group()
def main():
  """A CLI tool for Declarative Pipelines."""
  pass


@main.command()
@click.option(
    "--path",
    required=True,
    type=click.STRING,
    help=(
        "Target a specific YAML file or a directory to be recursively "
        "scanned for validation."
    ),
)
@click.option(
    "--model-version",
    required=False,
    type=click.STRING,
    help=(
        "Select the model version (e.g., 'v1', 'v2') to enforce against "
        "the provided YAML files."
    ),
)
def validate(path, model_version):
  """Validates the specified YAML file or all YAML files

  in specified directory.
  """

  path_obj = Path(path).resolve()
  if not path_obj.exists():
    click.echo(click.style(f"Error: Path does not exist: {path}", fg="red"))
    return

  if path_obj.is_dir():
    # Use rglob to recursively find all YAML files in
    # the directory and subdirectories.
    yaml_files = list(path_obj.rglob("*.yaml")) + list(path_obj.rglob("*.yml"))
  else:
    yaml_files = [path_obj]

  if not yaml_files:
    click.echo(click.style(f"No YAML files found in '{path}'.", fg="yellow"))
    return

  for yaml_file in yaml_files:
    try:
      with open(yaml_file, "r", encoding="utf-8") as f:
        definition = yaml.safe_load(f)

      if not definition:
        click.echo(
            click.style(f"⚠️  Skipping empty file: {yaml_file}", fg="yellow")
        )
        continue

      # 1. Extract the version from the YAML content
      version = definition.get("model_version")
      if not version:
        version = model_version

      # 2. Select the model dynamically
      model = MODEL_MAP.get(str(version).lower())
      if not model:
        click.echo(
            click.style(
                f"Unsupported model version: '{version}' in {yaml_file}. "
                f"Supported: {list(MODEL_MAP.keys())}",
                fg="red",
            )
        )
        continue

      # 3. Validate
      model.model_validate(definition)
      click.echo(
          click.style(
              f"✅ {yaml_file.name} (Version: {version}): Valid", fg="green"
          )
      )

    except ValidationError as e:
      handle_validation_error(e, yaml_file)
    except Exception as e:
      raise e


def handle_validation_error(e: ValidationError, file_path: Path):
  """Parses Pydantic ValidationError into a readable CLI output."""
  click.echo(
      click.style(
          f"\n❌ Validation failed for: {file_path}", fg="red", bold=True
      )
  )

  for error in e.errors():
    location = " -> ".join(str(loc) for loc in error["loc"])
    message = error["msg"]
    input_provided = error.get("input", "None")

    click.echo(
        click.style("  Field: ", fg="cyan")
        + click.style(location, fg="white", bold=True)
    )
    click.echo(click.style("  Error: ", fg="yellow") + f"{message}")

    # Optional: Print the invalid value if it's not a huge dict
    if not isinstance(input_provided, dict):
      click.echo(
          click.style("  Current value: ", fg="white", dim=True)
          + f"{input_provided}"
      )

    click.echo(click.style("  " + "-" * 20, fg="white", dim=True))


if __name__ == "__main__":
  main()
