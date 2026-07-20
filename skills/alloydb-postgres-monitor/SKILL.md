---
name: alloydb-postgres-monitor
description: Use these skills when you need to troubleshoot slow performance, analyze query execution plans, identify resource-heavy processes, and monitor system-level PromQL metrics.
metadata:
  version: v1
  publisher: google
license: Apache-2.0
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and `<param_value>` with actual values.

**Bash:**
`node <skill_dir>/scripts/<script_name>.js '{"<param_name>": "<param_value>"}'`

**PowerShell:**
`node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\": \"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env files. Do not ask the user to set vars unless skill executions fails due to env var absence.


## Scripts


### get_query_metrics

Fetches query level cloudmonitoring data (timeseries metrics) for queries running in an AlloyDB instance.
To use this tool, you must provide the Google Cloud `projectId` and a PromQL `query`.

Generate the PromQL `query` for AlloyDB query metrics using the provided metrics and rules. Get labels like `cluster_id`, `instance_id`, and `query_hash` from the user's intent. If `query_hash` is provided, use the per-query metrics.

Defaults:
1. Interval: Use a default interval of `5m` for `_over_time` aggregation functions unless a different window is specified by the user.

PromQL Query Examples:
1. Basic Time Series: `avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance"}[5m])`
2. Top K: `topk(30, avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance"}[5m]))`
3. Mean: `avg(avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="my-instance","cluster_id"="my-cluster"}[5m]))`
4. Minimum: `min(min_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance","cluster_id"="alloydb-cluster"}[5m]))`
5. Maximum: `max(max_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance","cluster_id"="alloydb-cluster"}[5m]))`
6. Sum: `sum(avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance","cluster_id"="alloydb-cluster"}[5m]))`
7. Count streams: `count(avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance","cluster_id"="alloydb-cluster"}[5m]))`
8. Percentile with groupby on instanceid, clusterid: `quantile by ("instance_id","cluster_id")(0.99,avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","cluster_id"="my-cluster","instance_id"="my-instance"}[5m]))`

Available Metrics List: metricname. description. monitored resource. labels. aggregate is the aggregated values for all query stats, Use aggregate metrics if query id is not provided. For perquery metrics do not fetch querystring unless specified by user specifically. Have the aggregation on query hash to avoid fetching the querystring. Do not use latency metrics for anything.
1. `alloydb.googleapis.com/database/postgresql/insights/aggregate/latencies`: Aggregated query latency distribution. `alloydb.googleapis.com/Database`. `user`, `client_addr`.
2. `alloydb.googleapis.com/database/postgresql/insights/aggregate/execution_time`: Accumulated aggregated query execution time since the last sample. `alloydb.googleapis.com/Database`. `user`, `client_addr`.
3. `alloydb.googleapis.com/database/postgresql/insights/aggregate/io_time`: Accumulated aggregated IO time since the last sample. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `io_type`.
4. `alloydb.googleapis.com/database/postgresql/insights/aggregate/lock_time`: Accumulated aggregated lock wait time since the last sample. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `lock_type`.
5. `alloydb.googleapis.com/database/postgresql/insights/aggregate/row_count`: Aggregated number of retrieved or affected rows since the last sample. `alloydb.googleapis.com/Database`. `user`, `client_addr`.
6. `alloydb.googleapis.com/database/postgresql/insights/aggregate/shared_blk_access_count`: Aggregated shared blocks accessed by statement execution. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `access_type`.
7. `alloydb.googleapis.com/database/postgresql/insights/perquery/latencies`: Per query latency distribution. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `querystring`, `query_hash`.
8. `alloydb.googleapis.com/database/postgresql/insights/perquery/execution_time`: Accumulated execution times per user per database per query. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `querystring`, `query_hash`.
9. `alloydb.googleapis.com/database/postgresql/insights/perquery/io_time`: Accumulated IO time since the last sample per query. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `io_type`, `querystring`, `query_hash`.
10. `alloydb.googleapis.com/database/postgresql/insights/perquery/lock_time`: Accumulated lock wait time since the last sample per query. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `lock_type`, `querystring`, `query_hash`.
11. `alloydb.googleapis.com/database/postgresql/insights/perquery/row_count`: The number of retrieved or affected rows since the last sample per query. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `querystring`, `query_hash`.
12. `alloydb.googleapis.com/database/postgresql/insights/perquery/shared_blk_access_count`: Shared blocks accessed by statement execution per query. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `access_type`, `querystring`, `query_hash`.
13. `alloydb.googleapis.com/database/postgresql/insights/pertag/latencies`: Query latency distribution. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`, `framework`, `route`, `tag_hash`.
14. `alloydb.googleapis.com/database/postgresql/insights/pertag/execution_time`: Accumulated execution times since the last sample. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`, `framework`, `route`, `tag_hash`.
15. `alloydb.googleapis.com/database/postgresql/insights/pertag/io_time`: Accumulated IO time since the last sample per tag. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`, `framework`, `route`, `io_type`, `tag_hash`.
16. `alloydb.googleapis.com/database/postgresql/insights/pertag/lock_time`: Accumulated lock wait time since the last sample per tag. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`, `framework`, `route`, `lock_type`, `tag_hash`.
17. `alloydb.googleapis.com/database/postgresql/insights/pertag/shared_blk_access_count`: Shared blocks accessed by statement execution per tag. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`, `framework`, `route`, `access_type`, `tag_hash`.
18. `alloydb.googleapis.com/database/postgresql/insights/pertag/row_count`: The number of retrieved or affected rows since the last sample per tag. `alloydb.googleapis.com/Database`. `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`, `framework`, `route`, `tag_hash`.


#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| projectId | string | The Id of the Google Cloud project. | Yes |  |
| query | string | The promql query to execute. | Yes |  |


---

### get_query_plan

Generate a PostgreSQL EXPLAIN plan in JSON format for a single SQL statement—without executing it. This returns the optimizer's estimated plan, costs, and rows (no ANALYZE, no extra options). Use in production safely for plan inspection, regression checks, and query tuning workflows.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| query | string | The SQL statement for which you want to generate plan (omit the EXPLAIN keyword). | Yes |  |


---

### get_system_metrics

Fetches system level cloudmonitoring data (timeseries metrics) for an AlloyDB cluster, instance.
To use this tool, you must provide the Google Cloud `projectId` and a PromQL `query`.

Generate the PromQL `query` for AlloyDB system metrics using the provided metrics and rules. Get labels like `cluster_id` and `instance_id` from the user's intent.

Defaults:
1. Interval: Use a default interval of `5m` for `_over_time` aggregation functions unless a different window is specified by the user.

PromQL Query Examples:
1. Basic Time Series: `avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance"}[5m])`
2. Top K: `topk(30, avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance"}[5m]))`
3. Mean: `avg(avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="my-instance","cluster_id"="my-cluster"}[5m]))`
4. Minimum: `min(min_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance","cluster_id"="alloydb-cluster"}[5m]))`
5. Maximum: `max(max_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance","cluster_id"="alloydb-cluster"}[5m]))`
6. Sum: `sum(avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance","cluster_id"="alloydb-cluster"}[5m]))`
7. Count streams: `count(avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","instance_id"="alloydb-instance","cluster_id"="alloydb-cluster"}[5m]))`
8. Percentile with groupby on instanceid, clusterid: `quantile by ("instance_id","cluster_id")(0.99,avg_over_time({"__name__"="alloydb.googleapis.com/instance/cpu/average_utilization","monitored_resource"="alloydb.googleapis.com/Instance","cluster_id"="my-cluster","instance_id"="my-instance"}[5m]))`

Available Metrics List: metricname. description. monitored resource. labels
1. `alloydb.googleapis.com/instance/cpu/average_utilization`: The percentage of CPU being used on an instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
2. `alloydb.googleapis.com/instance/cpu/maximum_utilization`: Maximum CPU utilization across all currently serving nodes of the instance from 0 to 100. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
3. `alloydb.googleapis.com/cluster/storage/usage`: The total AlloyDB storage in bytes across the entire cluster. `alloydb.googleapis.com/Cluster`. `cluster_id`.
4. `alloydb.googleapis.com/instance/postgres/replication/replicas`: The number of read replicas connected to the primary instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`, `state`, `replica_instance_id`.
5. `alloydb.googleapis.com/instance/postgres/replication/maximum_lag`: The maximum replication time lag calculated across all serving read replicas of the instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`, `replica_instance_id`.
6. `alloydb.googleapis.com/instance/memory/min_available_memory`: The minimum available memory across all currently serving nodes of the instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
7. `alloydb.googleapis.com/instance/postgres/instances`: The number of nodes in the instance, along with their status, which can be either up or down. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`, `status`.
8. `alloydb.googleapis.com/database/postgresql/tuples`: Number of tuples (rows) by state per database in the instance. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`, `state`.
9. `alloydb.googleapis.com/database/postgresql/temp_bytes_written_for_top_databases`: The total amount of data(in bytes) written to temporary files by the queries per database for top 500 dbs. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`.
10. `alloydb.googleapis.com/database/postgresql/temp_files_written_for_top_databases`: The number of temporary files used for writing data per database while performing internal algorithms like join, sort etc for top 500 dbs. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`.
11. `alloydb.googleapis.com/database/postgresql/inserted_tuples_count_for_top_databases`: The total number of rows inserted per db for top 500 dbs as a result of the queries in the instance. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`.
12. `alloydb.googleapis.com/database/postgresql/updated_tuples_count_for_top_databases`: The total number of rows updated per db for top 500 dbs as a result of the queries in the instance. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`.
13. `alloydb.googleapis.com/database/postgresql/deleted_tuples_count_for_top_databases`: The total  number of rows deleted per db for top 500 dbs as a result of the queries in the instance. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`.
14. `alloydb.googleapis.com/database/postgresql/backends_for_top_databases`: The current number of connections per database to the instance for top 500 dbs. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`.
15. `alloydb.googleapis.com/instance/postgresql/backends_by_state`: The current number of connections to the instance grouped by the state like idle, active, idle_in_transaction, idle_in_transaction_aborted, disabled, and fastpath_function_call. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`, `state`.
16. `alloydb.googleapis.com/instance/postgresql/backends_for_top_applications`: The current number of connections to the AlloyDB instance, grouped by applications for top 500 applications. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`, `application_name`.
17. `alloydb.googleapis.com/database/postgresql/new_connections_for_top_databases`: Total number of new connections added per database for top 500 databases to the instance. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`.
18. `alloydb.googleapis.com/database/postgresql/deadlock_count_for_top_databases`: Total number of deadlocks detected in the instance per database for top 500 dbs. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`.
19. `alloydb.googleapis.com/database/postgresql/statements_executed_count`: Total count of statements executed in the instance per database per operation_type. `alloydb.googleapis.com/Database`. `cluster_id`, `instance_id`, `database`, `operation_type`.
20. `alloydb.googleapis.com/instance/postgresql/returned_tuples_count`: Number of rows scanned while processing the queries in the instance since the last sample. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
21. `alloydb.googleapis.com/instance/postgresql/fetched_tuples_count`: Number of rows fetched while processing the queries in the instance since the last sample. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
22. `alloydb.googleapis.com/instance/postgresql/updated_tuples_count`: Number of rows updated while processing the queries in the instance since the last sample. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
23. `alloydb.googleapis.com/instance/postgresql/inserted_tuples_count`: Number of rows inserted while processing the queries in the instance since the last sample. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
24. `alloydb.googleapis.com/instance/postgresql/deleted_tuples_count`: Number of rows deleted while processing the queries in the instance since the last sample. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
25. `alloydb.googleapis.com/instance/postgresql/written_tuples_count`: Number of rows written while processing the queries in the instance since the last sample. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
26. `alloydb.googleapis.com/instance/postgresql/deadlock_count`: Number of deadlocks detected in the instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
27. `alloydb.googleapis.com/instance/postgresql/blks_read`: Number of blocks read by Postgres that were not in the buffer cache. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
28. `alloydb.googleapis.com/instance/postgresql/blks_hit`: Number of times Postgres found the requested block in the buffer cache. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
29. `alloydb.googleapis.com/instance/postgresql/temp_bytes_written_count`: The total amount of data(in bytes) written to temporary files by the queries while performing internal algorithms like join, sort etc. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
30. `alloydb.googleapis.com/instance/postgresql/temp_files_written_count`: The number of temporary files used for writing data in the instance while performing internal algorithms like join, sort etc. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
31. `alloydb.googleapis.com/instance/postgresql/new_connections_count`: The number new connections added to the instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.
32. `alloydb.googleapis.com/instance/postgresql/wait_count`: Total number of times processes waited for each wait event in the instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`, `wait_event_type`, `wait_event_name`.
33. `alloydb.googleapis.com/instance/postgresql/wait_time`: Total elapsed wait time for each wait event in the instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`, `wait_event_type`, `wait_event_name`.
34. `alloydb.googleapis.com/instance/postgres/transaction_count`: The number of committed and rolled back transactions across all serving nodes of the instance. `alloydb.googleapis.com/Instance`. `cluster_id`, `instance_id`.


#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| projectId | string | The Id of the Google Cloud project. | Yes |  |
| query | string | The promql query to execute. | Yes |  |


---

### list_active_queries

List the top N (default 50) currently running queries (state='active') from pg_stat_activity, ordered by longest-running first. Returns pid, user, database, application_name, client_addr, state, wait_event_type/wait_event, backend/xact/query start times, computed query_duration, and the SQL text.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| min_duration | string | Optional: Only show queries running at least this long (e.g., '1 minute', '1 second', '2 seconds'). | No | `1 minute` |
| exclude_application_names | string | Optional: A comma-separated list of application names to exclude from the query results. This is useful for filtering out queries from specific applications (e.g., 'psql', 'pgAdmin', 'DBeaver'). The match is case-sensitive. Whitespace around commas and names is automatically handled. If this parameter is omitted, no applications are excluded. | No | `` |
| limit | integer | Optional: The maximum number of rows to return. | No | `50` |


---

### list_database_stats



#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| database_name | string | Optional: A specific database name pattern to search for. | No | `` |
| include_templates | boolean | Optional: Whether to include template databases in the results. | No | `false` |
| database_owner | string | Optional: A specific database owner name pattern to search for. | No | `` |
| default_tablespace | string | Optional: A specific default tablespace name pattern to search for. | No | `` |
| order_by | string | Optional: The field to order the results by. Valid values are 'size' and 'commit'. | No | `` |
| limit | integer | Optional: The maximum number of rows to return. | No | `10` |


---

### list_locks

Identifies all locks held by active processes showing the process ID, user, query text, and an aggregated list of all transactions and specific locks (relation, mode, grant status) associated with each process.



---

### list_query_stats

Lists performance statistics for executed queries ordered by total time, filtering by database name pattern if provided. This tool requires the pg_stat_statements extension to be installed. The tool returns the database name, query text, execution count, timing metrics (total, min, max, mean), rows affected, and buffer cache I/O statistics (hits and reads).

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| database_name | string | Optional: The database name to list query stats for. | No | `` |
| limit | integer | Optional: The maximum number of results to return. Defaults to 50. | No | `50` |


---

### long_running_transactions

Identifies and lists database transactions that exceed a specified time limit. For each of the long running transactions, the output contains the process id, database name, user name, application name, client address, state, connection age, transaction age, query age, last activity age, wait event type, wait event, and query string.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| min_duration | string | Optional: Only show transactions running at least this long (e.g., '1 minute', '15 minutes', '30 seconds'). | No | `5 minutes` |
| limit | integer | Optional: The maximum number of long-running transactions to return. Defaults to 20. | No | `20` |


---

