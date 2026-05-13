---
name: gcp-dataflow
description: 'Provides guidance for writing, packaging and executing Apache Beam pipelines
  on GCP using Cloud Dataflow. Use when: - Creating an Apache Beam Dataflow pipeline.
  - Creating a Google Flex Template.

  '
license: Apache-2.0
metadata:
  version: v2
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

## Diagnostics & Troubleshooting

YOU MUST use this section when the user asks about performance of their dataflow
pipelines. This can be used to debug issues like pipeline slowness, pipeline
failures, etc.

### Task Execution Workflow

1.  **Understand User Request**: Extract Job ID, Project ID, Transform Name
    (optional), and Time Window.
2.  **Transform Name Mapping**: If the user requires transform-based debugging,
    map user-provided Transform Names to actual Dataflow `stage` or `ptransform`
    and apply to filters while querying:

    This mapping can be extracted from `gcloud dataflow jobs describe JOB_ID
    --full --format="json(pipelineDescription.executionPipelineStage)"`.

    1.  **Extract the targets**:
        *   Get stage_id: **`name`** property at the parent stage level. This
            matches `"F[digit]"` (e.g. `"F6"`).
        *   Get ptransform: inside the `componentTransform` array, read
            precisely from **`userName`** or **`originalTransform`** (e.g.
            `"RateLimitAndLog/ParMultiDo(RateLimitAndLog)"`). and use it as
            **`ptransform`**.
    2.  **Apply the filters strictly following mapping mechanics**:
        *   **For Cloud Logging queries**: Apply extracted ptransform name to
            filter `resource.labels.step_id="[Extracted ptransform name]"`.
        *   **For Monitoring queries**: Use the stage_id/ptransform filters
            based on filters supported by metric:
            `metric.labels.ptransform="[Extracted ptransform name]"` or
            `metric.labels.stage="[Extracted stage_id]"`.

3.  **Query Telemetry**:

    *   Use Dataflow REST API to get High level Job Messages/Events that
        happened in the job.
    *   Refer to
        [dataflow_diagnostics_reference.md](resources/dataflow_diagnostics_reference.md)
        for key metrics and logging query patterns based on Job Type.
    *   Use Monitoring REST API to fetch metrics.
    *   Use GCloud Logging command to fetch logs.
    *   Use Dataflow REST API to fetch current snapshot metrics when historical
        time-series are not needed.

4.  **Analysis**:

    *   Correlate metrics spikes/drops with log errors.
    *   Identify Issues.

5.  **Output**: Provide a synthesized summary with symptoms, potential root
    cause, and links to relevant code transforms (using `file:///...` format).
    Follow this template to structure your response:

    1.  High level Job Events: Infer from job messages.
    2.  Data Freshness: Infer from watermark_age/system_lag metrics.
    3.  Throughput: Infer from
        elements_produced_count/estimated_bytes_produced_count metrics.
    4.  Backlog: Infer from estimated_backlog_processing_time/backlog_bytes
        metrics.
    5.  Bottlenecks: Infer from is_bottleneck/backlogged_keys metrics.
    6.  Autoscaling: Infer from horizontal_worker_scaling metric.
    7.  Recommendations: Provide recommendations based on the analysis of both
        metrics and logs.
