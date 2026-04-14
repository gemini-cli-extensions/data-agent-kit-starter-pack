---
name: gcp-dataflow
description: 'Provides guidance for writing, packaging and executing Apache Beam pipelines
  on GCP using Cloud Dataflow. Use when: - Creating an Apache Beam Dataflow pipeline.
  - Creating a Google Flex Template.

  '
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

# Apache Beam Pipelines on Cloud Dataflow

Expert guidance for writing and packaging Apache Beam pipelines to run on Google
Cloud Dataflow.

## Creating a new project

Use this section when creating a new project for a Dataflow pipeline.

-   If the user doesn't say explicitly which language (Java, Python, Go) shall
    be used to write the pipeline, you MUST confirm the language.
-   Determine which version of Beam SDK should be used by searching for the most
    recently released version of Apache Beam, unless the user already uses a
    particular version.
    -   **Action**: Run a web search for the latest Apache Beam SDK release.
-   YOU MUST use same version of Apache Beam consistently throughout the project
    in Dockerfiles, `requirements.txt`, and other similar files where versions
    are specified.

### Java projects using Gradle

Use this section when configuring a Dataflow Java pipeline project using gradle.

-   **Shadow Jars (Fat Jars)**: Do NOT propose to use the Shadow plugin
    (`com.github.johnrengelman.shadow`) unless the user explicitly requests a
    Fat Jar.
-   **Passing command-line parameters**: Use the `application` plugin for
    passing command-line parameters.
-   **SLF4J Logging Dependency Alignment**:
    -   Verify the `slf4j-api` version pulled transitively by Apache Beam.
    -   You MUST configure the application logging backend (`slf4j-simple`,
        `logback-classic`, etc.) to exactly match the major/minor version of the
        resolved `slf4j-api`.

### Structure the pipeline as a Dataflow Flex Template

When creating new Dataflow pipeline projects, configure them as a Flex template.
Flex Templates offer a hermetic and reproducible launch environment, and are
easy to launch with `gcloud` or with orchestrators like Cloud Composer.

Follow the Flex Templates section below.

## Flex Templates

-   **Provide Instructions**: Provide instructions on rebuilding and running
    Flex Templates to the user in walkthrough.
-   **Use Single Docker Image for Python pipelines**: For Python Flex Templates,
    it is better to use a single image for the template launcher image and for
    the worker runtime environment (`--sdk_container_image`). Whenever
    configuring or suggesting a Dataflow Flex Template for a Python pipeline
    that requires extra dependencies (e.g., using `--requirements_file`,
    `--setup_file`, or `--extra_package`), **YOU MUST recommend the Single
    Docker Image Configuration** as detailed in
    [python_flex_template_reference.md](resources/python_flex_template_reference.md).
-   **Prefer Cloud Build over Local Docker**:
    -   Do NOT assume local Docker availability on the workspace machine.
    -   **Action**: Suggest and provide `cloudbuild.yaml` out-of-the-box for
        building and pushing images unless local setup is explicitly requested.
    -   When building images with Cloud Build in the background you MUST provide
        the link where the user can monitor the long-running operation.

## Launching Apache Beam Pipelines with Dataflow Runner

-   When launching Python Pipelines without a Flex Template with
    `DataflowRunner`, you MUST scan the pipeline project directory for the
    following files:

    -   **`requirements.txt`**:
        -   If found, you MUST include `--requirements_file` pipeline option.
    -   **`setup.py`**:
        -   If found, you MUST include `--setup_file` pipeline option. This is
            critical if the pipeline uses local modules or packages.

-   When launching Python Pipelines with a Flex Template, if the Flex Template
    image is also the SDK Container image (Single Docker Image Configuration),
    then you MUST supply the image in the `sdk_container_image` parameter.

-   Confirm the launch command with the user.

### Lookup environment resources instead of using placeholder values

-   Avoid using generic placeholders (e.g., `your-gcp-project-id`) for GCP
    resources when drafting run scripts or configs. **Action**: If values are
    unknown, proactively run commands like `gcloud config get-value project` to
    find active resources to pre-fill scripts for the user. Confirm the values
    with the user before proceeding.
