# Definitive Guide to reading and writing tables using spark code

> [!IMPORTANT]
> You MUST ALWAYS follow the Task Execution Workflow when writing spark code.

## Task Execution Workflow
1. Configure the spark session to read or write data from the required source or destination
2. Read or write the data from the required source or destination

## BigQuery

### Spark Session Configuration
No session configuration is needed to read from BigQuery, all jars and configuration are provided by default in Dataproc.

### Reading from BigQuery
#### Basic example to read a Big Query table
`df = spark.read.format("bigquery").option("table", "<PROJECT_ID>.<DATASET_NAME>.<TABLE_NAME>").load()`

#### Executing a BigQuery SQL query
The Spark BigQuery connector allows you to run Standard SQL SELECT queries directly on BigQuery and load the results into a spark dataframe.
> [!IMPORTANT] You must enable views option to run direct queries

```python
# Define Standard SQL query
sql = """
  SELECT name, SUM(number) as total
  FROM `bigquery-public-data.usa_names.usa_1910_2013`
  GROUP BY name
  LIMIT 10
"""

df = spark.read.format("bigquery").option("viewsEnabled", "true").load(sql)
```

#### BigQuery Join Patterns
When enriching data with BigQuery reference tables:

```python
# Read BigQuery table directly (connector is built-in)
reference_df = spark.read.format("bigquery") \
    .option("table", "<PROJECT_ID>.<DATASET_NAME>.<TABLE_NAME>") \
    .load()

# Join with your main DataFrame
enriched_df = main_df.join(
    reference_df.select("entity_id", "entity_name", "category"),
    on="entity_id",
    how="left"
)
```

#### Optimization Tips
1. Select only needed columns from BigQuery
```python
ref_df = spark.read.format("bigquery") \
    .option("table", "<PROJECT_ID>.<DATASET_NAME>.<LARGE_TABLE_NAME>") \
    .option("filter", "active = true") \
    .load() \
    .select("id", "name")
```

2. Using broadcast joins for small reference tables
```python
from pyspark.sql.functions import broadcast

enriched_df = main_df.join(
    broadcast(small_ref_df),  # < 10MB
    on="key"
)
```
3. Cache reference data if used multiple times, example: `ref_df.cache()`

### Writing to BigQuery

#### Non partitioned data
Write DataFrame to BigQuery using direct writes,
 - Set writeMethod to direct
 - Set mode to one of `overwrite`, `append`, `errorifexists` based on task
```python
df.write \
    .format("bigquery") \
    .option("table", "<PROJECT_ID>.<DATASET_NAME>.<TABLE_NAME>") \
    .option("writeMethod", "direct") \
    .mode("overwrite") \
    .save()
```
#### Parititioned data
Write DataFrame to a partitioned BigQuery table using indirect writes, in this method data is written to GCS first and then loaded into BigQuery. A gcs bucket is required as the temporary data location
 - Set temporaryGcsBucket to a gcs bucket name
 - Set a check point path location
```python
df.write \
  .format("bigquery") \
  .option("temporaryGcsBucket","<STAGING_GCS_BUCKET>") \
  .option("checkpointLocation", "<STAGING_PATH>") \
  .save("dataset.table")
```

## BigLake Iceberg Catalog

### Spark Session Configuration
- [!WARNING] BigLake Iceberg catalog must be configured in the spark session before tables can be read.
- Multiple Iceberg catalogs can be configured in the same spark session
- [!IMPORTANT] You **MUST** identify the storage layer for the BigLake Iceberg table before configuring the spark session. Use `@skill:discovering-gcp-data-assets` to **search** and **lookup** the table details. Check the value for the `metadataPath` field from the lookup results, if it starts with `gs:` proceed with GCS storage, if it starts with `s3:` then proceed with S3 storage.
- [!WARNING] **DO NOT** assume catalog_name, project_id, io implementation for a table, **ALWAYS lookup** table details before proceeding.

Example with GCS storage:
```python
spark = SparkSession.builder \
    .appName("<APP_NAME>") \
    .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
    .config('spark.sql.catalog.<GCS_CATALOG_NAME>', 'org.apache.iceberg.spark.SparkCatalog') \
    .config('spark.sql.catalog.<GCS_CATALOG_NAME>.type', 'rest') \
    .config('spark.sql.catalog.<GCS_CATALOG_NAME>.uri', 'https://biglake.googleapis.com/iceberg/v1/restcatalog') \
    .config('spark.sql.catalog.<GCS_CATALOG_NAME>.warehouse', 'gs://<GCS_CATALOG_NAME>') \
    .config('spark.sql.catalog.<GCS_CATALOG_NAME>.header.x-goog-user-project', '<CATALOG_PROJECT_ID>') \
    .config('spark.sql.catalog.<GCS_CATALOG_NAME>.rest.auth.type', 'org.apache.iceberg.gcp.auth.GoogleAuthManager') \
    .config('spark.sql.catalog.<GCS_CATALOG_NAME>.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
    .config('spark.sql.catalog.<GCS_CATALOG_NAME>.rest-metrics-reporting-enabled', 'false') \
    .getOrCreate()
```

Example with S3 storage:
```python
spark = SparkSession.builder \
    .appName("<APP_NAME>") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.<CATALOG_NAME>", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.<CATALOG_NAME>.type", "rest") \
    .config("spark.sql.catalog.<CATALOG_NAME>.uri", "https://biglake.googleapis.com/iceberg/v1/restcatalog") \
    .config("spark.sql.catalog.<CATALOG_NAME>.warehouse", f"bl://projects/<CATALOG_PROJECT_ID>/catalogs/<CATALOG_NAME>") \
    .config("spark.sql.catalog.<CATALOG_NAME>.header.x-goog-user-project", f"<CATALOG_PROJECT_ID>") \
    .config("spark.sql.catalog.<CATALOG_NAME>.rest.auth.type", "org.apache.iceberg.gcp.auth.GoogleAuthManager") \
    .config("spark.sql.catalog.<CATALOG_NAME>.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
    .config("spark.sql.catalog.<CATALOG_NAME>.rest-metrics-reporting-enabled", "false") \
    .config("spark.sql.catalog.<CATALOG_NAME>.header.X-Iceberg-Access-Delegation", "vended-credentials") \
    .config("spark.sql.catalog.<CATALOG_NAME>.s3.client-factory-impl", "org.apache.iceberg.aws.s3.DefaultS3FileIOAwsClientFactory") \
    .getOrCreate()
```

### Reading from BigLake Iceberg Catalog
- You **MUST** set the current spark catalog before attempting to read, using `spark.catalog.setCurrentCatalog("<CATALOG_NAME>")`. **DO NOT** use backticks in this call.
- [!IMPORTANT] You **MUST ALWAYS** surround the catalog name with backticks in SQL statements and `load()` calls to ensure proper handling of special characters (e.g., `catalog_name`).
```python
spark.catalog.setCurrentCatalog("<CATALOG_NAME>")
df = spark.read.format("iceberg").load("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>")
```

### Writing to BigLake Iceberg Catalog
[!IMPORTANT] Follow these instructions before writing code to write to BigLake iceberg tables
- **ALWAYS** use Spark's `DataFrameWriterV2` API (`writeTo`) for writing to Iceberg tables. This provides a richer API with specific write modes.
- You **MUST** set the current spark catalog before attempting to write, using `spark.catalog.setCurrentCatalog("<CATALOG_NAME>")`. **DO NOT** use backticks in this call.
- **ALWAYS** Ensure namespace is created before writing, using `spark.sql("CREATE NAMESPACE IF NOT EXISTS `<CATALOG_NAME>`.<NAMESPACE_NAME>")`
> [!IMPORTANT] You **MUST ALWAYS** surround the catalog name with backticks in SQL statements and `writeTo()` calls to ensure proper handling of special characters.
- [!WARNING] BigLake Iceberg catalog must be configured before tables can be read.
```python
# The basic pattern
spark.catalog.setCurrentCatalog("<CATALOG_NAME>")
df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>").using("iceberg")
```

#### Write Modes

- **DataFrameWriterV2 `createOrReplace()`**: Creates the table if it does not exist, or replaces it if it does.
    ```python
    df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>").using("iceberg").createOrReplace()
    ```

- **DataFrameWriterV2 `append()`**: Equivalent to `INSERT INTO`. Appends data to an existing table.
    ```python
    df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>").using("iceberg").append()
    ```
- **SPARK SQL MERGE INTO**: Performs row-level updates, inserts, and deletes by rewriting data files that contain affected rows. The source table can be persisted as a temp view to allow using it in the MERGE INTO statement. The source view and the target table must be joined on the primary key(s) to ensure correct row-level updates, inserts, and deletes.
    ```python
    df.createOrReplaceTempView("source_updates")

    spark.sql(f"""
        MERGE INTO `<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME> t
        USING source_updates s
        ON t.id = s.id
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)
    ```

- [!WARNING] These are less preferred write modes, use them ONLY if explicitly asked to:
*   **`create()`**: Equivalent to `CREATE TABLE AS SELECT`. Fails if the table already exists.
    ```python
    df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>").using("iceberg").create()
    ```
*   **`replace()`**: Equivalent to `REPLACE TABLE AS SELECT`.
    ```python
    df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>").using("iceberg").replace()
    ```
*   **`overwritePartitions()`**: Equivalent to dynamic `INSERT OVERWRITE`. Overwrites partitions in the table that match the data in the DataFrame.
    ```python
    df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>").using("iceberg").overwritePartitions()
    ```
*   **`overwrite(condition)`**: Overwrites data that matches a specific condition (e.g. static overwrite).
    ```python
    from pyspark.sql.functions import col
    df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>").using("iceberg").overwrite(col("level") == "INFO")
    ```

#### Advanced Iceberg Writes

##### Writing with partitions
Use partitioning transform functions if writing to partitioned tables using timestamp fields. Ex: years, months, days, hours etc.
Example: 
```python
from pyspark.sql.functions import days

df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>") \
    .using("iceberg") \
    .partitionedBy("level", days("ts")) \
    .createOrReplace()
```

##### Schema Evolution
Iceberg supports safe schema evolution. You can merge schema changes during an append.
```python
df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>").option("mergeSchema", "true").append()
```

##### Writing to a Specific Branch
```python
# To insert into an `audit` branch
df.writeTo("`<CATALOG_NAME>`.<NAMESPACE_NAME>.<TABLE_NAME>.branch_audit").append()
```

## Google Cloud Storage (GCS)
No session configuration is needed to read from GCS, all jars and configuration are provided by default in Dataproc.

### Reading from GCS

#### CSV format
Read with `header` and `inferSchema` without these, the header row becomes data and all columns are strings
`df = spark.read.option("header", "true").option("inferSchema", "true").csv("gs://<BUCKET>/<PATH_TO_CSV>")`

#### Parquet format
`df = spark.read.parquet("gs://<BUCKET>/<PATH_TO_PARQUET>")`

#### Json format
`df = spark.read.json("gs://<BUCKET>/<PATH_TO_JSON>")`

### Writing to GCS

#### Csv format
`df.write.csv("gs://bucket/output_path")`

#### Model artifacts
```python
# Warehouse already includes gs://, don't add it again
model_path = f"{spark.conf.get(f'spark.sql.catalog.{CATALOG}.warehouse')}/models/my_model"
model.write().overwrite().save(model_path)
```

## Spanner
### Spark Session Configuration
The spanner jar must be configured in the spark session before tables can be read. In the notebook code we can ONLY validate the spanner connector is configured.
Example:
```python
spark = SparkSession.builder \
    .appName("<APP_NAME>") \
    .config("spark.jars.packages", "gs://spark-lib/spanner/spark-3.5-spanner-1.3.0.jar") \
    .getOrCreate()
```

#### Reading Spanner tables
```python
df = spark.read.format('cloud-spanner') \
  .option("projectId", "<PROJECT_ID>") \
  .option("instanceId", "<INSTANCE_ID>") \
  .option("databaseId", "<DATABASE_ID>") \
  .option("table", "<TABLE_NAME>")
  .load()
```

### Writing to Spanner
**CRITICAL**: The connector support for writes is ; use the Python client instead.
**SOLUTION**: The native Python `google-cloud-spanner` library inside `mapPartitions`.

```python
def write_to_spanner(iterator):
    from google.cloud import spanner
    # ... See examples/config_b_inference_spanner.py
```
> [!CAUTION]
> **Timestamp Handling is Source-Dependent!**
> - **BigQuery**: Returns timestamps as **strings** (e.g., `"2026-01-10 02:45:59.486457 UTC"`)
> - **Iceberg**: Returns timestamps as **Python `datetime.datetime` objects**
> - **Spanner**: Requires **Python `datetime.datetime` objects**
>
> You **MUST** use a universal handler that checks the type before converting.

#### Universal Timestamp Converter (REQUIRED)

```python
import datetime

def ensure_datetime(ts_value):
    """
    Converts any timestamp representation to a Python datetime object.
    
    Handles:
    - None -> Returns current UTC time (or None if preferred)
    - datetime.datetime -> Passes through (Iceberg source)
    - str -> Parses common formats (BigQuery source)
    """
    if ts_value is None:
        return datetime.datetime.now(datetime.timezone.utc)
    
    if isinstance(ts_value, datetime.datetime):
        # Already a datetime (Iceberg source) - pass through
        return ts_value
    
    # String conversion (BigQuery source)
    ts_str = str(ts_value).replace(' UTC', '').strip()
    formats = [
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
    ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(ts_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Could not parse timestamp: {ts_value}")
```

#### Spanner Write Pattern

```python
def write_to_spanner(iterator):
    from google.cloud import spanner
    import datetime

    client = spanner.Client(project="<PROJECT_ID>")
    database = client.instance("<INSTANCE_ID>").database("<DATABASE_ID>")

    batch_rows = []
    for row in iterator:
        # ALWAYS use ensure_datetime() for timestamp columns
        ts_val = ensure_datetime(row.timestamp)

        batch_rows.append((row.id, row.amount, ts_val))

        if len(batch_rows) >= 500:
            with database.batch() as batch:
                batch.insert_or_update("<TABLE_NAME>", ["id", "amount", "ts"], batch_rows)
            batch_rows = []

    # Flush remaining
    if batch_rows:
        with database.batch() as batch:
            batch.insert_or_update("<TABLE_NAME>", ["id", "amount", "ts"], batch_rows)

    yield len(batch_rows)

df.rdd.mapPartitions(write_to_spanner).collect()
```