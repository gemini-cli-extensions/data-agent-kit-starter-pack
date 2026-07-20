---
name: cloud-sql-postgres-health
description: Use these skills when you need to audit database health, identify storage bloat, find invalid indexes, analyze table statistics, and manage maintenance configurations like autovacuum.
metadata:
  version: v1
  publisher: google
license: Apache-2.0
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and
`<param_value>` with actual values.

**Bash:** `node <skill_dir>/scripts/<script_name>.js '{"<param_name>":
"<param_value>"}'`

**PowerShell:** `node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\":
\"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env
files. Do not ask the user to set vars unless skill executions fails due to env
var absence.

## Scripts

### get_query_metrics

Fetches query level cloudmonitoring data (timeseries metrics) for queries
running in Postgres instance using a PromQL query. Take projectID and instanceID
from the user for which the metrics timeseries data needs to be fetched. To use
this tool, you must provide the Google Cloud `projectId` and a PromQL `query`.

Generate PromQL `query` for Postgres query metrics. Use the provided metrics and
rules to construct queries, Get the labels like `instance_id`, `query_hash` from
user intent. If query_hash is provided then use the per_query metrics. Query
hash and query id are same.

Defaults:

1.  Interval: Use a default interval of `5m` for `_over_time` aggregation
    functions unless a different window is specified by the user.

PromQL Query Examples:

1.  Basic Time Series:
    `avg_over_time({"__name__"="cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m])`
2.  Top K: `topk(30,
    avg_over_time({"__name__"="cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
3.  Mean:
    `avg(avg_over_time({"__name__"="cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
4.  Minimum:
    `min(min_over_time({"__name__"="cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
5.  Maximum:
    `max(max_over_time({"__name__"="cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
6.  Sum:
    `sum(avg_over_time({"__name__"="cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
7.  Count streams:
    `count(avg_over_time({"__name__"="cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
8.  Percentile with groupby on resource_id, database: `quantile by
    ("resource_id","database")(0.99,avg_over_time({"__name__"="cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`

Available Metrics List: metricname. description. monitored resource. labels.
resource_id label format is `project_id:instance_id` which is actually instance
id only. aggregate is the aggregated values for all query stats, Use aggregate
metrics if query id is not provided. For perquery metrics do not fetch
querystring unless specified by user specifically. Have the aggregation on query
hash to avoid fetching the querystring. Do not use latency metrics for anything.

1.  `cloudsql.googleapis.com/database/postgresql/insights/aggregate/latencies`:
    Aggregated query latency distribution. `cloudsql_instance_database`. `user`,
    `client_addr`, `project_id`, `resource_id`.
2.  `cloudsql.googleapis.com/database/postgresql/insights/aggregate/execution_time`:
    Accumulated aggregated query execution time since the last sample.
    `cloudsql_instance_database`. `user`, `client_addr`, `project_id`,
    `resource_id`.
3.  `cloudsql.googleapis.com/database/postgresql/insights/aggregate/io_time`:
    Accumulated aggregated IO time since the last sample.
    `cloudsql_instance_database`. `user`, `client_addr`, `io_type`,
    `project_id`, `resource_id`.
4.  `cloudsql.googleapis.com/database/postgresql/insights/aggregate/lock_time`:
    Accumulated aggregated lock wait time since the last sample.
    `cloudsql_instance_database`. `user`, `client_addr`, `lock_type`,
    `project_id`, `resource_id`.
5.  `cloudsql.googleapis.com/database/postgresql/insights/aggregate/row_count`:
    Aggregated number of retrieved or affected rows since the last sample.
    `cloudsql_instance_database`. `user`, `client_addr`, `project_id`,
    `resource_id`.
6.  `cloudsql.googleapis.com/database/postgresql/insights/aggregate/shared_blk_access_count`:
    Aggregated shared blocks accessed by statement execution.
    `cloudsql_instance_database`. `user`, `client_addr`, `access_type`,
    `project_id`, `resource_id`.
7.  `cloudsql.googleapis.com/database/postgresql/insights/perquery/latencies`:
    Per query latency distribution. `cloudsql_instance_database`. `user`,
    `client_addr`, `querystring`, `query_hash`, `project_id`, `resource_id`.
8.  `cloudsql.googleapis.com/database/postgresql/insights/perquery/execution_time`:
    Accumulated execution times per user per database per query.
    `cloudsql_instance_database`. `user`, `client_addr`, `querystring`,
    `query_hash`, `project_id`, `resource_id`.
9.  `cloudsql.googleapis.com/database/postgresql/insights/perquery/io_time`:
    Accumulated IO time since the last sample per query.
    `cloudsql_instance_database`. `user`, `client_addr`, `io_type`,
    `querystring`, `query_hash`, `project_id`, `resource_id`.
10. `cloudsql.googleapis.com/database/postgresql/insights/perquery/lock_time`:
    Accumulated lock wait time since the last sample per query.
    `cloudsql_instance_database`. `user`, `client_addr`, `lock_type`,
    `querystring`, `query_hash`, `project_id`, `resource_id`.
11. `cloudsql.googleapis.com/database/postgresql/insights/perquery/row_count`:
    The number of retrieved or affected rows since the last sample per query.
    `cloudsql_instance_database`. `user`, `client_addr`, `querystring`,
    `query_hash`, `project_id`, `resource_id`.
12. `cloudsql.googleapis.com/database/postgresql/insights/perquery/shared_blk_access_count`:
    Shared blocks accessed by statement execution per query.
    `cloudsql_instance_database`. `user`, `client_addr`, `access_type`,
    `querystring`, `query_hash`, `project_id`, `resource_id`.
13. `cloudsql.googleapis.com/database/postgresql/insights/pertag/latencies`:
    Query latency distribution. `cloudsql_instance_database`. `user`,
    `client_addr`, `action`, `application`, `controller`, `db_driver`,
    `framework`, `route`, `tag_hash`, `project_id`, `resource_id`.
14. `cloudsql.googleapis.com/database/postgresql/insights/pertag/execution_time`:
    Accumulated execution times since the last sample.
    `cloudsql_instance_database`. `user`, `client_addr`, `action`,
    `application`, `controller`, `db_driver`, `framework`, `route`, `tag_hash`,
    `project_id`, `resource_id`.
15. `cloudsql.googleapis.com/database/postgresql/insights/pertag/io_time`:
    Accumulated IO time since the last sample per tag.
    `cloudsql_instance_database`. `user`, `client_addr`, `action`,
    `application`, `controller`, `db_driver`, `framework`, `route`, `io_type`,
    `tag_hash`, `project_id`, `resource_id`.
16. `cloudsql.googleapis.com/database/postgresql/insights/pertag/lock_time`:
    Accumulated lock wait time since the last sample per tag.
    `cloudsql_instance_database`. `user`, `client_addr`, `action`,
    `application`, `controller`, `db_driver`, `framework`, `route`, `lock_type`,
    `tag_hash`, `project_id`, `resource_id`.
17. `cloudsql.googleapis.com/database/postgresql/insights/pertag/shared_blk_access_count`:
    Shared blocks accessed by statement execution per tag.
    `cloudsql_instance_database`. `user`, `client_addr`, `action`,
    `application`, `controller`, `db_driver`, `framework`, `route`,
    `access_type`, `tag_hash`, `project_id`, `resource_id`.
18. `cloudsql.googleapis.com/database/postgresql/insights/pertag/row_count`: The
    number of retrieved or affected rows since the last sample per tag.
    `cloudsql_instance_database`. `user`, `client_addr`, `action`,
    `application`, `controller`, `db_driver`, `framework`, `route`, `tag_hash`,
    `project_id`, `resource_id`.

#### Parameters

Name      | Type   | Description                         | Required | Default
:-------- | :----- | :---------------------------------- | :------- | :------
projectId | string | The Id of the Google Cloud project. | Yes      |
query     | string | The promql query to execute.        | Yes      |

--------------------------------------------------------------------------------

### get_query_plan

Generate a PostgreSQL EXPLAIN plan in JSON format for a single SQL
statement—without executing it. This returns the optimizer's estimated plan,
costs, and rows (no ANALYZE, no extra options). Use in production safely for
plan inspection, regression checks, and query tuning workflows.

#### Parameters

| Name  | Type   | Description                          | Required | Default |
| :---- | :----- | :----------------------------------- | :------- | :------ |
| query | string | The SQL statement for which you want | Yes      |         |
:       :        : to generate plan (omit the EXPLAIN   :          :         :
:       :        : keyword).                            :          :         :

--------------------------------------------------------------------------------

### get_system_metrics

Fetches system level cloudmonitoring data (timeseries metrics) for a Postgres
instance using a PromQL query. Take projectId and instanceId from the user for
which the metrics timeseries data needs to be fetched. To use this tool, you
must provide the Google Cloud `projectId` and a PromQL `query`.

Generate PromQL `query` for Postgres system metrics. Use the provided metrics
and rules to construct queries, Get the labels like `instance_id` from user
intent.

Defaults:

1.  Interval: Use a default interval of `5m` for `_over_time` aggregation
    functions unless a different window is specified by the user.

PromQL Query Examples:

1.  Basic Time Series:
    `avg_over_time({"__name__"="cloudsql.googleapis.com/database/cpu/utilization","monitored_resource"="cloudsql_database","project_id"="my-projectId","database_id"="my-projectId:my-instanceId"}[5m])`
2.  Top K: `topk(30,
    avg_over_time({"__name__"="cloudsql.googleapis.com/database/cpu/utilization","monitored_resource"="cloudsql_database","project_id"="my-projectId","database_id"="my-projectId:my-instanceId"}[5m]))`
3.  Mean:
    `avg(avg_over_time({"__name__"="cloudsql.googleapis.com/database/cpu/utilization","monitored_resource"="cloudsql_database","project_id"="my-projectId","database_id"="my-projectId:my-instanceId"}[5m]))`
4.  Minimum:
    `min(min_over_time({"__name__"="cloudsql.googleapis.com/database/cpu/utilization","monitored_resource"="cloudsql_database","project_id"="my-projectId","database_id"="my-projectId:my-instanceId"}[5m]))`
5.  Maximum:
    `max(max_over_time({"__name__"="cloudsql.googleapis.com/database/cpu/utilization","monitored_resource"="cloudsql_database","project_id"="my-projectId","database_id"="my-projectId:my-instanceId"}[5m]))`
6.  Sum:
    `sum(avg_over_time({"__name__"="cloudsql.googleapis.com/database/cpu/utilization","monitored_resource"="cloudsql_database","project_id"="my-projectId","database_id"="my-projectId:my-instanceId"}[5m]))`
7.  Count streams:
    `count(avg_over_time({"__name__"="cloudsql.googleapis.com/database/cpu/utilization","monitored_resource"="cloudsql_database","project_id"="my-projectId","database_id"="my-projectId:my-instanceId"}[5m]))`
8.  Percentile with groupby on database_id: `quantile by
    ("database_id")(0.99,avg_over_time({"__name__"="cloudsql.googleapis.com/database/cpu/utilization","monitored_resource"="cloudsql_database","project_id"="my-projectId","database_id"="my-projectId:my-instanceId"}[5m]))`

Available Metrics List: metricname. description. monitored resource. labels.
database_id is actually the instance id and the format is
`project_id:instance_id`.

1.  `cloudsql.googleapis.com/database/postgresql/new_connection_count`: Count of
    new connections added to the postgres instance. `cloudsql_database`.
    `database`, `project_id`, `database_id`.
2.  `cloudsql.googleapis.com/database/postgresql/backends_in_wait`: Number of
    backends in wait in postgres instance. `cloudsql_database`. `backend_type`,
    `wait_event`, `wait_event_type`, `project_id`, `database_id`.
3.  `cloudsql.googleapis.com/database/postgresql/transaction_count`: Delta count
    of number of transactions. `cloudsql_database`. `database`,
    `transaction_type`, `project_id`, `database_id`.
4.  `cloudsql.googleapis.com/database/memory/components`: Memory stats
    components in percentage as usage, cache and free memory for the database.
    `cloudsql_database`. `component`, `project_id`, `database_id`.
5.  `cloudsql.googleapis.com/database/postgresql/external_sync/max_replica_byte_lag`:
    Replication lag in bytes for Postgres External Server (ES) replicas.
    Aggregated across all DBs on the replica. `cloudsql_database`. `project_id`,
    `database_id`.
6.  `cloudsql.googleapis.com/database/cpu/utilization`: Current CPU utilization
    represented as a percentage of the reserved CPU that is currently in use.
    Values are typically numbers between 0.0 and 1.0 (but might exceed 1.0).
    Charts display the values as a percentage between 0% and 100% (or more).
    `cloudsql_database`. `project_id`, `database_id`.
7.  `cloudsql.googleapis.com/database/disk/bytes_used_by_data_type`: Data
    utilization in bytes. `cloudsql_database`. `data_type`, `project_id`,
    `database_id`.
8.  `cloudsql.googleapis.com/database/disk/read_ops_count`: Delta count of data
    disk read IO operations. `cloudsql_database`. `project_id`, `database_id`.
9.  `cloudsql.googleapis.com/database/disk/write_ops_count`: Delta count of data
    disk write IO operations. `cloudsql_database`. `project_id`, `database_id`.
10. `cloudsql.googleapis.com/database/postgresql/num_backends_by_state`: Number
    of connections to the Cloud SQL PostgreSQL instance, grouped by its state.
    `cloudsql_database`. `database`, `state`, `project_id`, `database_id`.
11. `cloudsql.googleapis.com/database/postgresql/num_backends`: Number of
    connections to the Cloud SQL PostgreSQL instance. `cloudsql_database`.
    `database`, `project_id`, `database_id`.
12. `cloudsql.googleapis.com/database/network/received_bytes_count`: Delta count
    of bytes received through the network. `cloudsql_database`. `project_id`,
    `database_id`.
13. `cloudsql.googleapis.com/database/network/sent_bytes_count`: Delta count of
    bytes sent through the network. `cloudsql_database`. `destination`,
    `project_id`, `database_id`.
14. `cloudsql.googleapis.com/database/postgresql/deadlock_count`: Number of
    deadlocks detected for this database. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
15. `cloudsql.googleapis.com/database/postgresql/blocks_read_count`: Number of
    disk blocks read by this database. The source field distingushes actual
    reads from disk versus reads from buffer cache. `cloudsql_database`.
    `database`, `source`, `project_id`, `database_id`.
16. `cloudsql.googleapis.com/database/postgresql/tuples_processed_count`: Number
    of tuples(rows) processed for a given database for operations like insert,
    update or delete. `cloudsql_database`. `operation_type`, `database`,
    `project_id`, `database_id`.
17. `cloudsql.googleapis.com/database/postgresql/tuple_size`: Number of tuples
    (rows) in the database. `cloudsql_database`. `database`, `tuple_state`,
    `project_id`, `database_id`.
18. `cloudsql.googleapis.com/database/postgresql/vacuum/oldest_transaction_age`:
    Age of the oldest transaction yet to be vacuumed in the Cloud SQL PostgreSQL
    instance, measured in number of transactions that have happened since the
    oldest transaction. `cloudsql_database`. `oldest_transaction_type`,
    `project_id`, `database_id`.
19. `cloudsql.googleapis.com/database/replication/log_archive_success_count`:
    Number of successful attempts for archiving replication log files.
    `cloudsql_database`. `project_id`, `database_id`.
20. `cloudsql.googleapis.com/database/replication/log_archive_failure_count`:
    Number of failed attempts for archiving replication log files.
    `cloudsql_database`. `project_id`, `database_id`.
21. `cloudsql.googleapis.com/database/postgresql/transaction_id_utilization`:
    Current utilization represented as a percentage of transaction IDs consumed
    by the Cloud SQL PostgreSQL instance. Values are typically numbers between
    0.0 and 1.0. Charts display the values as a percentage between 0% and 100% .
    `cloudsql_database`. `project_id`, `database_id`.
22. `cloudsql.googleapis.com/database/postgresql/num_backends_by_application`:
    Number of connections to the Cloud SQL PostgreSQL instance, grouped by
    applications. `cloudsql_database`. `application`, `project_id`,
    `database_id`.
23. `cloudsql.googleapis.com/database/postgresql/tuples_fetched_count`: Total
    number of rows fetched as a result of queries per database in the PostgreSQL
    instance. `cloudsql_database`. `database`, `project_id`, `database_id`.
24. `cloudsql.googleapis.com/database/postgresql/tuples_returned_count`: Total
    number of rows scanned while processing the queries per database in the
    PostgreSQL instance. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
25. `cloudsql.googleapis.com/database/postgresql/temp_bytes_written_count`:
    Total amount of data (in bytes) written to temporary files by the queries
    per database. `cloudsql_database`. `database`, `project_id`, `database_id`.
26. `cloudsql.googleapis.com/database/postgresql/temp_files_written_count`:
    Total number of temporary files used for writing data while performing
    algorithms such as join and sort. `cloudsql_database`. `database`,
    `project_id`, `database_id`.

#### Parameters

Name      | Type   | Description                         | Required | Default
:-------- | :----- | :---------------------------------- | :------- | :------
projectId | string | The Id of the Google Cloud project. | Yes      |
query     | string | The promql query to execute.        | Yes      |

--------------------------------------------------------------------------------

### list_active_queries

List the top N (default 50) currently running queries (state='active') from
pg_stat_activity, ordered by longest-running first. Returns pid, user, database,
application_name, client_addr, state, wait_event_type/wait_event,
backend/xact/query start times, computed query_duration, and the SQL text.

#### Parameters

| Name                      | Type    | Description     | Required | Default |
| :------------------------ | :------ | :-------------- | :------- | :------ |
| min_duration              | string  | Optional: Only  | No       | `1      |
:                           :         : show queries    :          : minute` :
:                           :         : running at      :          :         :
:                           :         : least this long :          :         :
:                           :         : (e.g., '1       :          :         :
:                           :         : minute', '1     :          :         :
:                           :         : second', '2     :          :         :
:                           :         : seconds').      :          :         :
| exclude_application_names | string  | Optional: A     | No       | ``      |
:                           :         : comma-separated :          :         :
:                           :         : list of         :          :         :
:                           :         : application     :          :         :
:                           :         : names to        :          :         :
:                           :         : exclude from    :          :         :
:                           :         : the query       :          :         :
:                           :         : results. This   :          :         :
:                           :         : is useful for   :          :         :
:                           :         : filtering out   :          :         :
:                           :         : queries from    :          :         :
:                           :         : specific        :          :         :
:                           :         : applications    :          :         :
:                           :         : (e.g., 'psql',  :          :         :
:                           :         : 'pgAdmin',      :          :         :
:                           :         : 'DBeaver'). The :          :         :
:                           :         : match is        :          :         :
:                           :         : case-sensitive. :          :         :
:                           :         : Whitespace      :          :         :
:                           :         : around commas   :          :         :
:                           :         : and names is    :          :         :
:                           :         : automatically   :          :         :
:                           :         : handled. If     :          :         :
:                           :         : this parameter  :          :         :
:                           :         : is omitted, no  :          :         :
:                           :         : applications    :          :         :
:                           :         : are excluded.   :          :         :
| limit                     | integer | Optional: The   | No       | `50`    |
:                           :         : maximum number  :          :         :
:                           :         : of rows to      :          :         :
:                           :         : return.         :          :         :

--------------------------------------------------------------------------------

### list_database_stats

#### Parameters

| Name               | Type    | Description              | Required | Default |
| :----------------- | :------ | :----------------------- | :------- | :------ |
| database_name      | string  | Optional: A specific     | No       | ``      |
:                    :         : database name pattern to :          :         :
:                    :         : search for.              :          :         :
| include_templates  | boolean | Optional: Whether to     | No       | `false` |
:                    :         : include template         :          :         :
:                    :         : databases in the         :          :         :
:                    :         : results.                 :          :         :
| database_owner     | string  | Optional: A specific     | No       | ``      |
:                    :         : database owner name      :          :         :
:                    :         : pattern to search for.   :          :         :
| default_tablespace | string  | Optional: A specific     | No       | ``      |
:                    :         : default tablespace name  :          :         :
:                    :         : pattern to search for.   :          :         :
| order_by           | string  | Optional: The field to   | No       | ``      |
:                    :         : order the results by.    :          :         :
:                    :         : Valid values are 'size'  :          :         :
:                    :         : and 'commit'.            :          :         :
| limit              | integer | Optional: The maximum    | No       | `10`    |
:                    :         : number of rows to        :          :         :
:                    :         : return.                  :          :         :

--------------------------------------------------------------------------------

### list_locks

Identifies all locks held by active processes showing the process ID, user,
query text, and an aggregated list of all transactions and specific locks
(relation, mode, grant status) associated with each process.

--------------------------------------------------------------------------------

### list_query_stats

Lists performance statistics for executed queries ordered by total time,
filtering by database name pattern if provided. This tool requires the
pg_stat_statements extension to be installed. The tool returns the database
name, query text, execution count, timing metrics (total, min, max, mean), rows
affected, and buffer cache I/O statistics (hits and reads).

#### Parameters

| Name          | Type    | Description                  | Required | Default |
| :------------ | :------ | :--------------------------- | :------- | :------ |
| database_name | string  | Optional: The database name  | No       | ``      |
:               :         : to list query stats for.     :          :         :
| limit         | integer | Optional: The maximum number | No       | `50`    |
:               :         : of results to return.        :          :         :
:               :         : Defaults to 50.              :          :         :

--------------------------------------------------------------------------------

### long_running_transactions

Identifies and lists database transactions that exceed a specified time limit.
For each of the long running transactions, the output contains the process id,
database name, user name, application name, client address, state, connection
age, transaction age, query age, last activity age, wait event type, wait event,
and query string.

#### Parameters

| Name         | Type    | Description                | Required | Default     |
| :----------- | :------ | :------------------------- | :------- | :---------- |
| min_duration | string  | Optional: Only show        | No       | `5 minutes` |
:              :         : transactions running at    :          :             :
:              :         : least this long (e.g., '1  :          :             :
:              :         : minute', '15 minutes', '30 :          :             :
:              :         : seconds').                 :          :             :
| limit        | integer | Optional: The maximum      | No       | `20`        |
:              :         : number of long-running     :          :             :
:              :         : transactions to return.    :          :             :
:              :         : Defaults to 20.            :          :             :

--------------------------------------------------------------------------------
