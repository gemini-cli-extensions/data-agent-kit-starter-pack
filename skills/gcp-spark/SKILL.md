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
    any code. Do NOT guess column names. When resource names (project, instance,
    database, table) are provided in the task:
    *   **Call tools with full scoping arguments**: Spanner tools require both
        `instance_id` and `database_id`; BigQuery tools require `project_id` and
        `dataset_id`. If a tool call returns `INVALID_ARGUMENT`, verify and fix
        your argument parameters before abandoning the tool.
    *   **Instance scanning as fallback**: Scanning across instances in a
        project is allowed when resource names are unknown or when a correctly
        formatted direct check returns `NOT_FOUND`. Prior to scanning, you
        **MUST** attempt direct tool or single-shot CLI calls using the exact
        parameters provided.
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
5.  **Compile code before executing**: **ALWAYS** verify syntax for any
    generated PySpark `.py` script by running `python3 -m py_compile script.py`
    BEFORE uploading to GCS or submitting to Dataproc. For notebooks, convert
    them to a python script first using `jupyter nbconvert --to script
    your-notebook.ipynb` and then run `python3 -m py_compile your-notebook.py`.
6.  **Execute script**: ONLY when generating a `.py` script refer to
    `references/gcloud_dataproc.md` on writing command to execute generated code
    on Dataproc. Provide standard `--jars` and
    `--properties="spark.jars.packages=..."` flags for Dataproc Serverless batch
    submission whenever connecting to Spanner, Postgres, Iceberg, or Pub/Sub.
    This DOES NOT apply when generating notebooks.

--------------------------------------------------------------------------------

## General Rule: 3-Part Qualified Table Names (`catalog.schema.table`)

> [!IMPORTANT] When encountering 3-part table identifiers in PySpark SQL or
> BigLake/Iceberg contexts (e.g. `catalog_name.namespace.table_name`): - **Do
> NOT assume the first identifier is a GCP Project ID.** In Spark SQL with
> catalog extensions, `cat_name.db_name.tbl_name` specifies the **Spark Catalog
> Name**, not a GCP project. - **Project ID Resolution:** GCP infrastructure
> resources (Dataproc, BigQuery, Spanner, GCS) reside in the target GCP Project
> ID passed via `--project` or environment configuration. NEVER pass a Spark
> catalog name (e.g., `ag_eval_test`) as `project_id` to BigQuery API tools or
> `gcloud` commands. - **Direct PySpark Querying:** Query the catalog table
> directly using `spark.read.table("catalog_name.namespace.table_name")` in
> PySpark SQL. Do NOT engage in exploratory project listing loops.

--------------------------------------------------------------------------------

## Common Mistakes Checklist

> [!CAUTION]
>
> Ensure you verify this checklist to avoid mistakes

Before submitting a job, verify:

-   [ ] **Syntax compilation verified** ALWAYS run `python3 -m py_compile
    script.py` to check for syntax errors before uploading to GCS or submitting
    to Dataproc
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
-   [ ] **Dataproc Serverless connector flags provided** pass required `--jars`
    and `--properties="spark.jars.packages=..."` flags for Spanner, Postgres,
    Iceberg, or Pub/Sub connections during batch submission. For Spanner pass
    `.option("projectId", "<PROJECT_ID>")`. Special delimiter escaping `^#^` or
    `\,` is required when multiple Maven packages are passed under
    `spark.jars.packages`.

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
