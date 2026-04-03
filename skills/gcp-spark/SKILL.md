---
name: gcp-spark
description: |
  Develops and executes Spark code on Dataproc Serverless.
  Read and write data using BigLake Iceberg catalogs, BigQuery and spanner.
  Debugs execution failures.
  Use when:
  - Writing Spark ETL pipelines on GCP.
  - Training or running inference with ML models with spark on GCP.
  Don't use when:
  - Writing generic Python scripts that don't use Spark.
  - Performing simple SQL queries that can be done directly in BigQuery.
license: TBD
metadata:
  version: v1
  publisher: google
---

# Spark on Dataproc Serverless

> [!IMPORTANT]
> You MUST ALWAYS follow the Task Execution Workflow when writing spark code.

## Task Execution Workflow

1.  **Understand schemas**: **ALWAYS** use `@skill:discovering-gcp-data-assets`
    skill or `resources/schema_direct_inspection.md` to understand input and
    output schemas. Include the schema in your thought process BEFORE generating
    any code. Do NOT guess column names.
2.  **Generate spark code**:
    *   **Output Format**: **ALWAYS** generate code in **Python Notebooks
        (.ipynb)** format. Generate scripts (.py) only if explicitly requested.
    *   **Read and Write data**: **ALWAYS** Refer to
        `resources/read_write_data.md` when reading or writing data.
    *   **ML Tasks**: Refer to `@skill:ml-best-practices` skill and
        `resources/ml_tasks.md` when generating ML code.
    *   **Spark Optimizations**: **ALWAYS** refer to
        `resources/spark_optimizations.md` when generating spark code and apply
        optimization whenever applicable.
3.  **Verify schema before write**: **ALWAYS** verify that the dataframe and
    destination schema match, use `df.printSchema()` for dataframe schema and
    refer to `@skill:discovering-gcp-data-assets` skill or
    `resources/schema_direct_inspection.md` to verify destination schema.
4.  **Compile code before executing**: For notebooks convert them to python
    script using `jupyter nbconvert --to script your-notebook.ipynb` first, then
    compile code using `python3 -m py_compile your-notebook.py`.
5.  **Execute script**: ONLY when generating a `.py` script refer to
    `resources/gcloud_dataproc.md` on writing command to execute generated code
    on Dataproc. This DOES NOT apply when generating notebooks.

--------------------------------------------------------------------------------

## Common Mistakes Checklist

![CAUTION] Ensure you verify this checklist to avoid mistakes

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

Role                         | For
---------------------------- | ------------------------
`roles/dataproc.worker`      | Job execution
`roles/biglake.admin`        | Iceberg table management
`roles/bigquery.jobUser`     | Query materialization
`roles/storage.objectUser`   | Read/write GCS
`roles/spanner.databaseUser` | Spanner writes
