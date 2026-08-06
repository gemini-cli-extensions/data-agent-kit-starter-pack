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

## Project and region/location preferences

Users configure `gcloud` to point at their desired project and region/location.
Assume gcloud is already installed.

Look up the configuration with:

```
gcloud config get project
gcloud config get dataproc/region
gcloud config get dataproc/location
gcloud config get compute/region
```

If region and location are not set, you may suggest using the compute region.

### Prefer MCP if possible

> [!IMPORTANT] If you have access to one or more MCP servers related to Dataproc
> or Serverless Spark, you MUST use those MCP tools rather than gcloud. ONLY
> fall back to gcloud if MCP tools are not available.

When using MCP, the ONLY thing you use gcloud for is looking up
project/region/location to pass as arguments to the MCP tools.

### gcloud as backup

If MCP servers are not available or there are no tools that can be used for your
use case, use `gcloud` to interact with Dataproc.

In general, Dataproc Clusters and Serverless Batches commands accept `--region`.
Dataproc Serverless Sessions commands accept `--location`.

## Dataproc Clusters

Use this section if the user requests "spark jobs", "spark clusters",
"clusters", "cluster jobs", or just "jobs". **Do not** use this section if the
user requests "serverless jobs", "serverless batches", or "batches".

### Listing clusters

Prefer MCP if available. If using gcloud, use this command template:

```
gcloud dataproc clusters list \
    --format="json(\
clusterName,\
clusterUuid,\
projectId,\
region,\
creator,\
status)" \
    --sort-by="~status.stateStartTime" \
    --limit=100
```

Tips:

-   **Important:** Always include a limit; the default is no limit, which may
    produce too much output to process.
-   Add a `--filter` to limit results, e.g. `status.state = ACTIVE AND
    clusterName = mycluster AND labels.env = staging AND labels.starred = *`

### Listing jobs

Prefer MCP if available. If using gcloud, use this command template:

```
gcloud dataproc jobs list \
    --format="json(\
jobType,\
reference,\
placement.clusterName,\
status.state,\
status.stateStartTime)" \
    --sort-by="~status.stateStartTime" \
    --limit=100
```

Tips:

-   **Important:** Always include a limit; the default is no limit, which may
    produce too much output to process.
-   Add a `--filter` to limit results, e.g. `status.state = ACTIVE AND
    labels.env = staging AND labels.starred = *`

## Dataproc Serverless

Use this section if the user requests:

-   batches, serverless batches, spark batches, serverless jobs
-   spark sessions, serverless spark sessions, spark interactive sessions,
    serverless interactive sessions, spark notebooks, spark kernels

**Do not** use this section if the user requests spark jobs, cluster jobs, or
just jobs, **unless** you have confirmed with the user that they are using
Serverless.

### Listing batches

Prefer MCP if available. If using gcloud, use this command template:

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

#### Basic batch submission command

Prefer MCP if available. If using gcloud, use this command template:

Augment the basic command with iceberg, spanner or xgboost related arguments as
needed by the script to be executed.

```
gcloud dataproc batches submit pyspark <SCRIPT_PATH.py> \
    --project=<PROJECT_ID> \
    --region=<GCP_REGION> \
    --version=2.3 \
    --deps-bucket=<GCS_PATH>
```

You MUST set the `--deps-bucket` to a GCS path to upload workload dependencies.

> [!IMPORTANT] Dataproc Serverless batches can be expected to take a very long
> time. **Typical initial execution time:** 10-15 minutes. This is **NORMAL**
> behavior. [!WARNING] **DO NOT CANCEL PREMATURELY!**

#### Reading or writing to BigLake Iceberg catalog

If the pyspark script is reading or writing data to BigLake Iceberg catalog. Set
these properties `--properties="\
spark.sql.catalog.<CATALOG_NAME>=org.apache.iceberg.spark.SparkCatalog,\
spark.sql.catalog.<CATALOG_NAME>.type=rest,\
spark.sql.catalog.<CATALOG_NAME>.uri=\
https://biglake.googleapis.com/iceberg/v1/restcatalog,\
spark.sql.catalog.<CATALOG_NAME>.io-impl=\
org.apache.iceberg.gcp.gcs.GCSFileIO,\
spark.sql.catalog.<CATALOG_NAME>.header.x-goog-user-project=<PROJECT_ID>,\
spark.sql.catalog.<CATALOG_NAME>.warehouse=<WAREHOUSE>,\
spark.sql.catalog.<CATALOG_NAME>.rest.auth.type=\
org.apache.iceberg.gcp.auth.GoogleAuthManager,\ spark.sql.extensions=\
org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"` If the
BigLake is GCS Catalog type then `WAREHOUSE="gs://<CATALOG_NAME>"`, if it's BQ
federated type then `WAREHOUSE="bq://projects/<PROJECT_ID>"`

#### Dataproc Serverless Connector Dependencies

> [!IMPORTANT] When submitting Dataproc Serverless batches that connect to
> Spanner, Postgres, Iceberg, or Pub/Sub, you MUST provide the appropriate
> `--jars` or `--properties="spark.jars.packages=..."` flags to ensure driver
> connectors are loaded.
>
> **Version Selection, Property Syntax & Compilation Notes:** - **Pre-Submission
> Syntax Compilation:** ALWAYS run `python3 -m py_compile <script.py>` locally
> to catch syntax errors BEFORE uploading to GCS or submitting a Dataproc
> batch. - **Check for Available Jars & Packages:** Check `gs://spark-lib/` for
> Google-provided jars or Maven Central for package coordinates. - **Spark
> Version Matching:** Dataproc Serverless 2.2 / 2.3 runs Spark 3.5. Ensure
> connector artifacts match Spark major.minor version 3.5 (e.g.,
> `spark-3.5-spanner-1.4.0.jar` or `iceberg-spark-runtime-3.5_2.12:1.5.0`). -
> **Package Property Flag & Delimiter Escaping:** In `gcloud dataproc batches
> submit pyspark`, Maven packages are specified via
> `--properties="spark.jars.packages=group:artifact:version"`. When combining
> multiple comma-separated packages in `spark.jars.packages`, escape commas with
> `\,` or use `^#^` custom delimiter syntax (e.g.
> `--properties="^#^spark.jars.packages=pkg1,pkg2#prop2=val2"`).

#### Spanner Connector

Include the Spark Spanner connector jar using `--jars`:

```
--jars=gs://spark-lib/spanner/spark-3.5-spanner-1.4.0.jar
```

*Note:* In PySpark, you MUST pass `.option("projectId", "<PROJECT_ID>")` along
with `instanceId`, `databaseId`, and `table`.

#### Cloud SQL PostgreSQL / Postgres Connector

Include the PostgreSQL JDBC driver package via `spark.jars.packages`:

```
--properties="spark.jars.packages=org.postgresql:postgresql:42.6.0"
```

*Note:* When connecting to private IP Cloud SQL instances, ensure the batch
submission includes `--subnet=default` (or your private Google Access subnet).

#### BigLake Iceberg Connector

Include the Iceberg Spark runtime package via `spark.jars.packages`:

```
--properties="spark.jars.packages=org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
```

Configure REST catalog properties:

```
--properties="\
spark.sql.catalog.<CATALOG_NAME>=org.apache.iceberg.spark.SparkCatalog,\
spark.sql.catalog.<CATALOG_NAME>.type=rest,\
spark.sql.catalog.<CATALOG_NAME>.uri=https://biglake.googleapis.com/iceberg/v1/restcatalog,\
spark.sql.catalog.<CATALOG_NAME>.io-impl=org.apache.iceberg.gcp.gcs.GCSFileIO,\
spark.sql.catalog.<CATALOG_NAME>.header.x-goog-user-project=<PROJECT_ID>,\
spark.sql.catalog.<CATALOG_NAME>.warehouse=gs://<WAREHOUSE_BUCKET>,\
spark.sql.catalog.<CATALOG_NAME>.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager,\
spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
```

*Note:* In Spark SQL, 3-part table names
`<CATALOG_NAME>.<NAMESPACE>.<TABLE_NAME>` specify the REST catalog name as the
first segment (`<CATALOG_NAME>`), NOT a GCP Project ID. Do NOT pass
`<CATALOG_NAME>` as a GCP `project_id` to BigQuery or `gcloud` CLI commands. If
catalog table resolution fails, fall back to direct reading from the GCS storage
path using `spark.read.parquet("gs://<bucket>/<path>")`.

#### Pub/Sub Integration

Standard Google Cloud Pub/Sub uses the `google.cloud.pubsub_v1` Python client
library (`from google.cloud import pubsub_v1`), which is pre-installed in the
Dataproc Serverless Python environment.

-   Do NOT pass non-existent `spark-3.5-pubsub` Maven package.
-   Create a temporary subscription to pull messages or publish messages
    directly using `pubsub_v1`.
-   For Pub/Sub Lite streaming, pass
    `--properties="spark.jars.packages=com.google.cloud:pubsublite-spark-sql-streaming:1.0.1"`.

#### Submitting Batches with Multiple Connector Dependencies

When submitting a PySpark script that connects to multiple data sources in a
single batch, combine all required `--jars` (comma-separated) and Maven packages
in `--properties="spark.jars.packages=pkg1,pkg2"`:

```
gcloud dataproc batches submit pyspark <SCRIPT_PATH.py> \
    --project=<PROJECT_ID> \
    --region=<GCP_REGION> \
    --version=2.3 \
    --subnet=default \
    --deps-bucket=<GCS_PATH> \
    --jars=gs://spark-lib/spanner/spark-3.5-spanner-1.4.0.jar \
    --properties="\
spark.jars.packages=org.postgresql:postgresql:42.6.0\,org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0,\
spark.sql.catalog.<CATALOG_NAME>=org.apache.iceberg.spark.SparkCatalog,\
spark.sql.catalog.<CATALOG_NAME>.type=rest,\
spark.sql.catalog.<CATALOG_NAME>.uri=https://biglake.googleapis.com/iceberg/v1/restcatalog,\
spark.sql.catalog.<CATALOG_NAME>.io-impl=org.apache.iceberg.gcp.gcs.GCSFileIO,\
spark.sql.catalog.<CATALOG_NAME>.header.x-goog-user-project=<PROJECT_ID>,\
spark.sql.catalog.<CATALOG_NAME>.warehouse=gs://<WAREHOUSE_BUCKET>,\
spark.sql.catalog.<CATALOG_NAME>.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager,\
spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
```

#### XGBoost

XGBoost requires spark dynamic allocation to be disabled. Set additional
properties:

```
--properties="spark.dynamicAllocation.enabled=false"
```

### Creating sessions

**Do not** create sessions using gcloud for use in notebooks. Instead, direct
the user to associate the notebook with a kernel using the Kernel Selector:

1.  Click "Remote Spark Kernels"
2.  Choose a kernel name ending in "on Serverless Spark"

It is expected for Serverless kernel creation to take approximately 2 minutes or
more.

### Listing sessions

Prefer MCP if available. If using gcloud, use this command template:

```
gcloud beta dataproc sessions list \
    --format="json(createTime, uuid, creator, state, jupyterSession, sparkConnectSession)" \
    --sort-by="~createTime" \
    --limit=100
```

Tips:

-   **Important:** Always include a limit; the default is no limit, which may
    produce too much output to process.
-   Add a `--filter` to limit results, e.g. `state = ACTIVE AND labels.env =
    staging AND create_time >= "2023-01-01T00:00:00Z"`
