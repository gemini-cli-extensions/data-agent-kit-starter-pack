# Dataproc and Spark Integration
Manage Spark resources on Google Cloud Dataproc Clusters and Serverless,
  including setting up clusters; launching jobs and batches; managing serverless
  session templates, and inspecting outputs.

## Background

Dataproc is Google Cloud's managed service for running Hadoop and Spark
workloads. The two basic flavors are:

-   **Clusters** aka **Dataproc on GCE**: users create a cluster, then submit
    one or more Spark or other jobs. Users have control over the underlying VM
    resources.
-   **Serverless Spark** aka **Dataproc Serverless**, where users do not control
    the underlying VM resources:
    -   Users may submit **batches**, which provision the underlying resources,
        launch a job, and tear down the resources, all in a single operation.
    -   Users may also create persistent **interactive sessions**. These are
        generally created through a Jupyter interface rather than gcloud, but
        existing sessions may be inspected with gcloud.
    -   Users can create **session templates** as a way to create multiple
        sessions using the same configuration.

Users may not always know the technically correct terminology for Clusters vs.
Serverless, for example they may ask for "jobs" or "spark jobs" but mean
Serverless Batches.

## Setup

-   Use `gcloud` to interact with Dataproc. Assume users have gcloud installed.

-   Assume gcloud is configured point at their desired project and region. You
    may look up the project and region with:

    ```
    gcloud config get project
    gcloud config get dataproc/region
    gcloud config get compute/region
    ```

    The region is taken from `dataproc/region` if present, otherwise falls back
    to `compute/region`.

## Dataproc Clusters

Use this section if the user requests "spark jobs", "spark clusters",
"clusters", "cluster jobs", or just "jobs". **Do not** use this section if the
user requests "serverless jobs", "serverless batches", or "batches".

### Listing clusters

Use this command template:

```
gcloud dataproc clusters list \
    --format="json(clusterName, clusterUuid, projectId, region, creator, status)"
    --sort-by="~status.stateStartTime" \
    --limit=100
```

Tips:

-   **Important:** Always include a limit; the default is no limit, which may
    produce too much output to process.
-   Add a `--filter` to limit results, e.g. `status.state = ACTIVE AND
    clusterName = mycluster AND labels.env = staging AND labels.starred = *`

### Listing jobs

Use this command template:

```
gcloud dataproc jobs list \
    --format="json(jobType, reference, placement.clusterName, status.state, status.stateStartTime)" \
    --sort-by="~status.stateStartTime" \
    --limit=100
```

Tips:

-   **Important:** Always include a limit; the default is no limit, which may
    produce too much output to process.
-   Add a `--filter` to limit results, e.g. `status.state = ACTIVE AND
    labels.env = staging AND labels.starred = *`

## Dataproc Serverless

Use this section if the user requests "batches", "serverless batches", "spark
batches", "serverless jobs". **Do not** use this section if the user requests
"spark jobs", "cluster jobs", or just "jobs", **unless** you have confirmed with
the user that they are using Serverless.

### Listing batches

Use this command template:

```
gcloud dataproc batches list \
    --format="json(batchType, createTime, creator, name, state, stateTime)" \
    --sort-by="~stateTime" \
    --limit=100
```

Tips:

-   **Important:** Always include a limit; the default is no limit, which may
    produce too much output to process.
-   Add a `--filter` to limit results, e.g. `(state = RUNNING and create_time <
    "2023-01-01T00:00:00Z") or labels.environment=production`

### Launching batches

> [!WARNING] This DOES NOT apply to executing **Python Notebooks (.ipynb)**.
> [!IMPORTANT] Refer to this guide when executing **PySpark Script (.py)** ONLY.

Determine the properties and configuration required by the pyspark script before
 executing the command for Job Submission

#### Basic Job submission command
Augment the basic command with iceberg, spanner or xgboost related arguments as
 needed by the script to be executed.
```bash
gcloud dataproc batches submit pyspark <SCRIPT_PATH.py> \
    --project=<PROJECT_ID> \
    --region=<GCP_REGION> \
    --version=2.3 \
    --deps-bucket=<GCS_PATH>
```
You MUST set the `--deps-bucket` to a GCS path to upload workload dependencies.

> [!IMPORTANT] Dataproc Serverless batches can be expected to take a very long
 time, **Typical initial execution time:**: 10-15 minutes. This is **NORMAL** behavior.
> [!WARNING]
> **DO NOT CANCEL PREMATURELY!**

#### Reading or writing to BigLake Iceberg catalog
If the pyspark script is reading or writing data to BigLake Iceberg catalog. Set
 these properties
```
--properties="\
    spark.sql.catalog.<CATALOG_NAME>=org.apache.iceberg.spark.SparkCatalog,\
    spark.sql.catalog.<CATALOG_NAME>.type=rest,\
    spark.sql.catalog.<CATALOG_NAME>.uri=https://biglake.googleapis.com/iceberg/v1/restcatalog,\
    spark.sql.catalog.<CATALOG_NAME>.io-impl=org.apache.iceberg.gcp.gcs.GCSFileIO,\
    spark.sql.catalog.<CATALOG_NAME>.header.x-goog-user-project=<PROJECT_ID>,\
    spark.sql.catalog.<CATALOG_NAME>.warehouse=<WAREHOUSE>\
    spark.sql.catalog.<CATALOG_NAME>.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager,\
    spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions,\
"
```
If the BigLake is GCS Catalog type then `WAREHOUSE="gs://<CATALOG_NAME>"`, if
 it's BQ federated type then `WAREHOUSE="bq://projects/<PROJECT_D>"`

## Reading data from spanner
Include the spark spanner connect jar using argument
 `--jars=gs://spark-lib/spanner/spark-3.5-spanner-1.2.2.jar`

## XGBoost
XGBoost requires spark dynamic allocation to be disabled. Set additional
 properties:
```
--properties="spark.dynamicAllocation.enabled=false"
```

