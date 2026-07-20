# Spark Optimizations

## Broadcast Joins

When performing a standard join between a large fact table and a tiny dimension
table (lookup table), always use a broadcast hint
`pyspark.sql.functions.broadcast()`. Without it, Spark may perform a heavy
shuffle operation and lead to performance issues or out-of-memory errors.
