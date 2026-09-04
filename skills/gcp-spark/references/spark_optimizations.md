# Spark Optimizations

## Broadcast Joins

When performing a standard join between a large fact table and a tiny dimension
table (lookup table), always use a broadcast hint
`pyspark.sql.functions.broadcast()`. Without it, Spark may perform a heavy
shuffle operation and lead to performance issues or out-of-memory errors.

## Driver Memory Protection

Never call `.toPandas()` or `.collect()` directly on full or un-aggregated
PySpark DataFrames to the driver process. Always perform cluster-side
aggregations (`groupBy().agg()`) or sampling (`.sample()`) to reduce data to a
small summary before converting to Pandas for plotting, display, or modeling.
