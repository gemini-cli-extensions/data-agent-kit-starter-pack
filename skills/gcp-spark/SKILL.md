---
name: gcp-spark
description: |
  Develops and executes Spark code on Dataproc Clusters and Serverless.
  Reads and writes data using BigLake Iceberg catalogs, BigQuery and Spanner.
  Debugs execution failures.
  Use when:
  - Writing Spark ETL pipelines on GCP.
  - Training or running inference with ML models with spark on GCP.
  - Managing Spark clusters, jobs, batches, and interactive sessions.
  Don't use when:
  - Writing generic Python scripts that don't use Spark.
  - Performing simple SQL queries that can be done directly in BigQuery.
license: Apache-2.0
metadata:
  version: v10
  publisher: google
---

# Spark on Dataproc

> [!IMPORTANT]
>
> You MUST ALWAYS follow the Task Execution Workflow when writing spark code.

## Task Execution Workflow

1.  **Understand schemas & Handle Typo Variants**: **ALWAYS** understand input
    and output schemas before generating any code. Include the schema in your
    thought process BEFORE generating any code. Do NOT guess column names.

    -   **Target Project Scope**: All assets MUST remain in the project and
        dataset specified by the user. Do NOT search across other GCP projects
        and NEVER switch to a different project or substitute tables from other
        projects (e.g. if user requested `sqlgen-testing.financial.loans`, do
        NOT use `datagravity-demo` or `cloud-db-nl2sql`).
    -   **Schema Direct Inspection & Typo Handling**: Refer to
        `references/schema_direct_inspection.md`. Note that on external or
        shared datasets, direct metadata operations (`bq ls` or `bq show`) and
        `INFORMATION_SCHEMA` queries may fail with `Access Denied` due to
        lacking metadata list permissions on foreign projects. Always test
        candidate table name variants (e.g. singular vs plural: `loan` for
        `loans`, `order` for `orders`, `account` for `accounts`) directly using
        `bq query`:

        ```bash
        bq query --use_legacy_sql=false "SELECT * FROM \`<TARGET_PROJECT>.<DATASET_ID>.<CANDIDATE_TABLE>\` LIMIT 1"
        ```

        *(e.g., ``bq query --use_legacy_sql=false "SELECT * FROM
        \`sqlgen-testing.financial.loan\` LIMIT 1"``)*

        Running `SELECT * FROM ... LIMIT 1` via `bq query` runs using the
        caller's active billing project, verifies table existence, and directly
        reveals the table schema and column names (e.g. `amount`, `loan_id`).

    -   **AUTONOMOUS TYPO CORRECTION RULE**: If the user-specified table name
        contains a likely typo or singular/plural mismatch (e.g., `loans` vs
        `loan`, `orders` vs `order`, `accounts` vs `account`), you MUST
        autonomously correct the typo to the canonical entity table name in the
        specified target project and dataset (e.g., use
        `sqlgen-testing.financial.loan` in `.option("table",
        "sqlgen-testing.financial.loan")`). ALWAYS generate and execute the
        PySpark notebook using the corrected table name (`loan`). NEVER revert
        back to the misspelled table name (`loans`) in the notebook code or
        markdown cells. Even if direct CLI queries return permission or
        environment errors in test sandboxes, you MUST proceed with generating
        and executing the notebook using the corrected table name
        (`sqlgen-testing.financial.loan`).

    -   *STRICT PROHIBITION*: NEVER call `bigquery__search_catalog` across other
        GCP projects, NEVER search or use tables in `datagravity-demo` or
        `cloud-db-nl2sql` when the user requested `sqlgen-testing`, and NEVER
        abandon the user's target project.
2.  **Verify source accessibility**: verify access/existence using `gcloud
    storage ls gs://<path-to-dataset>`. If accessing or reading a GCS path fails
    with a storage error e.g., permission errors like `403
    Forbidden`/`Forbidden`/`PermissionDenied`, or location errors like `404 Not
    Found`/`NotFound`/`FileNotFoundException` you should report the error
    immediately. Either (1) ask the user what to do next, or (2) if asked to
    execute a notebook, save the notebook with the error output and recommend
    next steps to resolve the issue. Do NOT scan all buckets for alternative
    fallback datasets when encountering GCS errors.
3.  **Generate spark code**:
    *   **Output Format**: **ALWAYS** generate code in **Python Notebooks
        (.ipynb)** format. Generate scripts (.py) only if explicitly requested.
    *   **Read and Write data**: **ALWAYS** Refer to
        `references/read_write_data.md` when reading or writing data.
    *   **ML Tasks**: Refer to `@skill:ml-best-practices` skill and
        `references/ml_tasks.md` when generating ML code.
    *   **Spark Optimizations**: **ALWAYS** refer to
        `references/spark_optimizations.md` when generating spark code and apply
        optimization whenever applicable.
4.  **Verify schema before write**: **ALWAYS** verify that the dataframe and
    destination schema match, use `df.printSchema()` for dataframe schema and
    refer to `references/schema_direct_inspection.md` to verify destination
    schema.
5.  **Compile code before executing**: For notebooks convert them to python
    script using `jupyter nbconvert --to script your-notebook.ipynb` first. Then
    compile the resulting python script using `python3 -m py_compile
    your-script.py`. The same can be done for pyspark source code.
6.  **Execute script**: When requested to run a job, script, session refer to
    `references/gcloud_dataproc.md` on how to execute generated code on Managed
    Spark. This DOES NOT apply when generating notebooks.

--------------------------------------------------------------------------------

## Common Mistakes Checklist

> [!CAUTION]
>
> Ensure you verify this checklist to avoid mistakes

Before submitting a job, verify:

-   [ ] **All imports present** (`col`, `when`, `lit`, etc. from
    `pyspark.sql.functions`)
-   [ ] **`vector_to_array` from correct module** use `from pyspark.ml.functions
    import vector_to_array` (NOT `pyspark.sql.functions`)
-   [ ] **DataFrame schema matches target Iceberg table** verify with
    `df.printSchema()` before writing
-   [ ] **CSV files read with `header` and `inferSchema`** without these, the
    header row becomes data and all columns are strings
-   [ ] **Driver memory safety (`toPandas()` / `collect()`)** NEVER call
    `.toPandas()` or `.collect()` on raw or un-aggregated DataFrames. ALWAYS
    perform transformations, aggregations (`groupBy().agg()`), or data reduction
    (`limit()`, `sample()`) in Spark before converting small summaries to Pandas
    for plotting or display.
-   [ ] **Target Dataset Typo Correction (`loan` vs `loans`)**: When a table
    read fails or `bq show` returns permission denied on external datasets,
    directly test singular/plural candidate variants using `bq query` (e.g. ``bq
    query --use_legacy_sql=false "SELECT * FROM
    \`sqlgen-testing.financial.loan\` LIMIT 1"``). Autonomously correct minor
    typos to the canonical entity table name in the target dataset (e.g. load
    `sqlgen-testing.financial.loan`) in the PySpark notebook `.option("table",
    "sqlgen-testing.financial.loan")`. NEVER revert back to the misspelled table
    name (`loans`) in the notebook code or markdown text. NEVER search across or
    substitute tables from other GCP projects.

--------------------------------------------------------------------------------

## IAM Requirements

The Dataproc service account needs:

*   `roles/dataproc.worker`: Job execution
*   `roles/biglake.admin`: Iceberg table management
*   `roles/bigquery.jobUser`: Query materialization
*   `roles/storage.objectUser`: Read/write GCS
*   `roles/spanner.databaseUser`: Spanner writes

--------------------------------------------------------------------------------

## Spark resource management

Refer to `references/gcloud_dataproc.md` for detailed guidelines on managing
Spark clusters, jobs, batches, and interactive sessions.
