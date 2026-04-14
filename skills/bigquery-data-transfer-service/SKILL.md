---
name: bigquery-data-transfer-service
description: Discovers and inspects BigQuery Data Transfer Service (DTS) configurations.
  Use this to identify existing ingestion pipelines and extract datasource or transfer
  config metadata for data pipelines. Use when a user asks for ingestion scenarios
  while building or managing data pipelines or when a user asks to "ingest" or "add"
  data that may already be managed by a DTS transfer.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

# BigQuery Data Transfer Service (DTS)

## Mandatory Guidelines

> [!IMPORTANT]
>
> All new BigQuery Data Transfer Service (DTS) configurations **MUST** be
> provisioned through the **gcp pipeline resource provisioning** framework,
> which includes generating a `deployment.yaml`.
>
> -   **Do NOT** use imperative CLI commands (e.g., `bq mk` or `gcloud`) to
>     create or update configurations.
> -   CLI commands are permitted **only** for discovery (listing/showing) and
>     triggering manual runs.

This guide enables the discovery of existing ingestion resources and provides
metadata related to ingestion when needed.

## Workflow

### Step 0: Check for Existing Transfers

Before assuming a new transfer is needed, check for existing ones in the target
region.

1.  **List Transfers**:

    ```bash
    bq ls --transfer_config \
      --transfer_location=[LOCATION] \
      --project_id=[PROJECT_ID]
    ```

2.  **Evaluate Results**:

    -   **Single Transfer Found**:

        -   Check if the transfer has at least one successful run: `bq ls
            --transfer_run --transfer_config=[RESOURCE_NAME]`
        -   If found: Use existing or manage via deployment framework.
        -   If not found: Guess tables from config.

    -   **Multiple Transfers Found**:

        -   Attempt to guess the correct one based on context.
        -   Ask user to confirm.

    -   **Disabled Transfers Found**:

        -   Ask user if they want to enable it or create a new one.
        -   Enable: `bq update --disabled=false
            --transfer_config=[RESOURCE_NAME]`

    -   **No Transfers Found**: Proceed to create new if needed.

### Step 1: Discover & Validate Parameters (New Transfers)

If creating a new transfer, discover the required parameters using the REST API
and validate them with the user.

> [!TIP] If `DATA_SOURCE_ID` is unknown, run `bq show --transfer_data_sources`
> `--location=[LOCATION] --project_id=[PROJECT_ID]` to list available source IDs
> (e.g., `google_cloud_storage`, `salesforce`).

1.  **Run Discovery Script**: Use the `bigquery_dts.py` script to inspect Data
    Source parameters via the REST API.

    ```bash
    # Use the path to the script in your workspace
    python3 scripts/bigquery_dts.py --project_id [PROJECT_ID] [DATA_SOURCE_ID] [LOCATION]
    ```

    > [!IMPORTANT] Run this command every time a new transfer is being planned.

2.  **Mandatory User Questionnaire (CRITICAL)**:

    -   Identify mandatory parameters.
    -   Present them to the user BEFORE generating config files.
    -   Ask for verification of assets/tables.

3.  **Wait for User Response**: Do NOT proceed until parameters are confirmed.

### Step 2: Extract Transfer Config Data

Retrieve the configuration details for the selected transfer.

```bash
bq show --format=prettyjson --transfer_config [RESOURCE_NAME]
```

### Step 3: Trigger and Verify Transfer

After the transfer is deployed via the resource provisioning framework, you MUST
ensure there is at least a single successful run before proceeding with the rest
of the tasks.

1.  **Trigger a Manual Run**: If no successful runs are found, or the transfer
    was just created, trigger a manual run for the current time.

    ```bash
    bq mk --transfer_run \
      --transfer_config=[RESOURCE_NAME] \
      --run_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    ```

2.  **Poll for Completion (5-Minute Rule)**: Attempt to check the status of the
    run every 30-60 seconds for up to **5 minutes**.

    ```bash
    bq ls --transfer_run --transfer_config=[RESOURCE_NAME]
    ```

    -   **Success**: If the run completes successfully, proceed with the rest of
        the pipeline.
    -   **Failure**: If the run fails, analyze the logs and ask the user for
        help.
    -   **Timeout (5 mins)**: If the run is still in progress after 5 minutes,
        **STOP** and ask the user: "The Data Transfer Service ingestion is still
        in progress. Please provide 'proceed guidance' once the ingestion has
        finished so that I can continue building the rest of the data pipeline
        using the ingested schema and samples."

3.  **Wait for User Guidance**: Do NOT proceed until the user confirms ingestion
    is complete or provides guidance.

4.  Once user confirms to proceed, start work on rest of the tasks.

## Definition of Done

-   A BigQuery DTS transfer configuration has been discovered or provisioned
    declaratively (via **gcp pipeline resource provisioning** with a generated
    `deployment.yaml`).
-   Mandatory datasource parameters have been identified and confirmed with the
    user.
-   A manual transfer run has been triggered and monitored.
-   The transfer run has completed successfully OR the user has provided
    "proceed guidance" for a long-running transfer.
