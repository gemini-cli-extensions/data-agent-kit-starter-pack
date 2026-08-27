# Spark Optimizations & Driver Safety

## 1. Broadcast Joins

When performing a standard join between a large fact table and a tiny dimension
table (lookup table), always use the `pyspark.sql.functions.broadcast()` hint.
Without it, Spark may perform a heavy shuffle operation and lead to performance
issues or out-of-memory errors:

```python
from pyspark.sql.functions import broadcast

df_joined = fact_df.join(broadcast(dim_df), "user_id", "left")
```

## 2. Adaptive Query Execution (AQE) & Coalesce Partitions

Always enable Adaptive Query Execution (AQE) in PySpark configurations. AQE
automatically optimizes shuffle partitions at runtime, handles data skew, and
coalesces tiny shuffle partitions:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

## 3. Small File Problem (GCS Output Buffering)

Writing raw DataFrames directly to Google Cloud Storage (GCS) can produce
thousands of tiny 1-KB files, severely degrading GCS metadata performance and
downstream read latency.

-   **Before `.write.parquet()` or `.write.saveAsTable()`**: Repartition or
    coalesce to produce optimal 128MB–512MB file sizes:

    ```python
    # Coalesce to a single partition for small output summaries
    summary_df.coalesce(1).write.mode("overwrite").parquet("gs://my-bucket/summary")

    # Repartition by logical partition keys before writing partitioned tables
    df.repartition(4, "year", "month").write.partitionBy("year", "month").parquet("gs://my-bucket/data")
    ```

## 4. Driver Out-Of-Memory (OOM) Safety

NEVER call `.toPandas()` or `.collect()` on raw or un-aggregated DataFrames. The
Spark Driver JVM node will crash with an Out-Of-Memory (OOM) exception if
millions of rows are pulled into driver memory.

-   **Always Aggregate or Limit**:

    ```python
    # SAFE: Aggregated summary before converting to Pandas for plotting
    pdf = df.groupBy("region").agg({"revenue": "sum"}).toPandas()

    # SAFE: Explicitly limited sample for previewing
    pdf = df.limit(500).toPandas()
    ```
