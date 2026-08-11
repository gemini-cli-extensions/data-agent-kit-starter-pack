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
  version: v4
  publisher: google
---

# Spark on Dataproc

> [!IMPORTANT]
>
> You MUST ALWAYS follow the Task Execution Workflow when writing spark code.

## Task Execution Workflow

1.  **Understand schemas**: **ALWAYS** use `@skill:discovering-gcp-data-assets`
    skill or `references/schema_direct_inspection.md` to understand input and
    output schemas. Include the schema in your thought process BEFORE generating
    any code. Do NOT guess column names. Unless explicitly specified, assume
    that the assets are located in the same project. Avoid scanning for assets
    across other projects as it can take a long time.
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
    refer to `@skill:discovering-gcp-data-assets` skill or
    `references/schema_direct_inspection.md` to verify destination schema.
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
-   [ ] **Avoid toPandas()** Converting a pyspark dataframe to pandas by calling
    toPandas() can lead to out of memory errors. Only acceptable for building
    visualizations in Spark 3.5

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
