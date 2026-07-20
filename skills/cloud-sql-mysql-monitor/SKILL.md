---
name: cloud-sql-mysql-monitor
description: Use these skills when you need to troubleshoot slow queries, analyze system-level PromQL metrics, and identify structural performance issues like table fragmentation or missing unique indexes.
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
running in Mysql instance using a PromQL query. Take projectID and instanceID
from the user for which the metrics timeseries data needs to be fetched. To use
this skill, you must provide the Google Cloud `projectId` and a PromQL `query`.

Generate PromQL `query` for Mysql query metrics. Use the provided metrics and
rules to construct queries, Get the labels like `instance_id`, `query_hash` from
user intent. If query_hash is provided then use the per_query metrics. Query
hash and query id are same.

Defaults:

1.  Interval: Use a default interval of `5m` for `_over_time` aggregation
    functions unless a different window is specified by the user.

PromQL Query Examples:

1.  Basic Time Series:
    `avg_over_time({"__name__"="dbinsights.googleapis.com/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m])`
2.  Top K: `topk(30,
    avg_over_time({"__name__"="dbinsights.googleapis.com/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
3.  Mean:
    `avg(avg_over_time({"__name__"="dbinsights.googleapis.com/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
4.  Minimum:
    `min(min_over_time({"__name__"="dbinsights.googleapis.com/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
5.  Maximum:
    `max(max_over_time({"__name__"="dbinsights.googleapis.com/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
6.  Sum:
    `sum(avg_over_time({"__name__"="dbinsights.googleapis.com/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
7.  Count streams:
    `count(avg_over_time({"__name__"="dbinsights.googleapis.com/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`
8.  Percentile with groupby on resource_id, database: `quantile by
    ("resource_id","database")(0.99,avg_over_time({"__name__"="dbinsights.googleapis.com/aggregate/execution_time","monitored_resource"="cloudsql_instance_database","project_id"="my-projectId","resource_id"="my-projectId:my-instanceId"}[5m]))`

Available Metrics List: metricname. description. monitored resource. labels.
resource_id label format is `project_id:instance_id` which is actually instance
id only. aggregate is the aggregated values for all query stats, Use aggregate
metrics if query id is not provided. For perquery metrics do not fetch
querystring unless specified by user specifically. Have the aggregation on query
hash to avoid fetching the querystring. Do not use latency metrics for anything.

1.  `dbinsights.googleapis.com/aggregate/latencies`: Cumulative query latency
    distribution per user and database. `cloudsql_instance_database`. `user`,
    `client_addr`, `database`, `project_id`, `resource_id`.
2.  `dbinsights.googleapis.com/aggregate/execution_time`: Cumulative query
    execution time per user and database. `cloudsql_instance_database`. `user`,
    `client_addr`, `database`, `project_id`, `resource_id`.
3.  `dbinsights.googleapis.com/aggregate/execution_count`: Total number of query
    executions per user and database. `cloudsql_instance_database`. `user`,
    `client_addr`, `database`, `project_id`, `resource_id`.
4.  `dbinsights.googleapis.com/aggregate/lock_time`: Cumulative lock wait time
    per user and database. `cloudsql_instance_database`. `user`, `client_addr`,
    `lock_type`, `database`, `project_id`, `resource_id`.
5.  `dbinsights.googleapis.com/aggregate/io_time`: Cumulative IO wait time per
    user and database. `cloudsql_instance_database`. `user`, `client_addr`,
    `database`, `project_id`, `resource_id`.
6.  `dbinsights.googleapis.com/aggregate/row_count`: Total number of rows
    affected during query execution. `cloudsql_instance_database`. `user`,
    `client_addr`, `row_status`, `database`, `project_id`, `resource_id`.
7.  `dbinsights.googleapis.com/perquery/latencies`: Cumulative query latency
    distribution per user, database, and query. `cloudsql_instance_database`.
    `querystring`, `user`, `client_addr`, `query_hash`, `database`,
    `project_id`, `resource_id`.
8.  `dbinsights.googleapis.com/perquery/execution_time`: Cumulative query
    execution time per user, database, and query. `cloudsql_instance_database`.
    `querystring`, `user`, `client_addr`, `query_hash`, `database`,
    `project_id`, `resource_id`.
9.  `dbinsights.googleapis.com/perquery/execution_count`: Total number of query
    executions per user, database, and query. `cloudsql_instance_database`.
    `querystring`, `user`, `client_addr`, `query_hash`, `database`,
    `project_id`, `resource_id`.
10. `dbinsights.googleapis.com/perquery/lock_time`: Cumulative lock wait time
    per user, database, and query. `cloudsql_instance_database`. `querystring`,
    `user`, `client_addr`, `lock_type`, `query_hash`, `database`, `project_id`,
    `resource_id`.
11. `dbinsights.googleapis.com/perquery/io_time`: Cumulative io wait time per
    user, database, and query. `cloudsql_instance_database`. `querystring`,
    `user`, `client_addr`, `query_hash`, `database`, `project_id`,
    `resource_id`.
12. `dbinsights.googleapis.com/perquery/row_count`: Total number of rows
    affected during query execution. `cloudsql_instance_database`.
    `querystring`, `user`, `client_addr`, `query_hash`, `row_status`,
    `database`, `project_id`, `resource_id`.
13. `dbinsights.googleapis.com/pertag/latencies`: Cumulative query latency
    distribution per user, database, and tag. `cloudsql_instance_database`.
    `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`,
    `framework`, `route`, `tag_hash`, `database`, `project_id`, `resource_id`.
14. `dbinsights.googleapis.com/pertag/execution_time`: Cumulative query
    execution time per user, database, and tag. `cloudsql_instance_database`.
    `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`,
    `framework`, `route`, `tag_hash`, `database`, `project_id`, `resource_id`.
15. `dbinsights.googleapis.com/pertag/execution_count`: Total number of query
    executions per user, database, and tag. `cloudsql_instance_database`.
    `user`, `client_addr`, `action`, `application`, `controller`, `db_driver`,
    `framework`, `route`, `tag_hash`, `database`, `project_id`, `resource_id`.
16. `dbinsights.googleapis.com/pertag/lock_time`: Cumulative lock wait time per
    user, database and tag. `cloudsql_instance_database`. `user`, `client_addr`,
    `action`, `application`, `controller`, `db_driver`, `framework`, `route`,
    `lock_type`, `tag_hash`, `database`, `project_id`, `resource_id`.
17. `dbinsights.googleapis.com/pertag/io_time`: Cumulative IO wait time per
    user, database and tag. `cloudsql_instance_database`. `user`, `client_addr`,
    `action`, `application`, `controller`, `db_driver`, `framework`, `route`,
    `tag_hash`, `database`, `project_id`, `resource_id`.
18. `dbinsights.googleapis.com/pertag/row_count`: Total number of rows affected
    during query execution. `cloudsql_instance_database`. `user`, `client_addr`,
    `action`, `application`, `controller`, `db_driver`, `framework`, `route`,
    `tag_hash`, `row_status`, `database`, `project_id`, `resource_id`.

#### Parameters

Name      | Type   | Description                         | Required | Default
:-------- | :----- | :---------------------------------- | :------- | :------
projectId | string | The Id of the Google Cloud project. | Yes      |
query     | string | The promql query to execute.        | Yes      |

--------------------------------------------------------------------------------

### get_query_plan

Provide information about how MySQL executes a SQL statement. Common use cases
include: 1) analyze query plan to improve its performance, and 2) determine
effectiveness of existing indexes and evalueate new ones.

#### Parameters

Name          | Type   | Description                   | Required | Default
:------------ | :----- | :---------------------------- | :------- | :------
sql_statement | string | The sql statement to explain. | Yes      |

--------------------------------------------------------------------------------

### get_system_metrics

Fetches system level cloudmonitoring data (timeseries metrics) for a MySQL
instance using a PromQL query. Take projectId and instanceId from the user for
which the metrics timeseries data needs to be fetched. To use this skill, you
must provide the Google Cloud `projectId` and a PromQL `query`.

Generate PromQL `query` for MySQL system metrics. Use the provided metrics and
rules to construct queries, Get the labels like `instance_id` from user intent.

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

1.  `cloudsql.googleapis.com/database/cpu/utilization`: Current CPU utilization
    as a percentage of reserved CPU. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
2.  `cloudsql.googleapis.com/database/network/connections`: Number of
    connections to the database instance. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
3.  `cloudsql.googleapis.com/database/network/received_bytes_count`: Delta count
    of bytes received through the network. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
4.  `cloudsql.googleapis.com/database/network/sent_bytes_count`: Delta count of
    bytes sent through the network. `cloudsql_database`. `destination`,
    `database`, `project_id`, `database_id`.
5.  `cloudsql.googleapis.com/database/memory/components`: Memory usage for
    components like usage, cache, and free memory. `cloudsql_database`.
    `component`, `database`, `project_id`, `database_id`.
6.  `cloudsql.googleapis.com/database/disk/bytes_used_by_data_type`: Data
    utilization in bytes. `cloudsql_database`. `data_type`, `database`,
    `project_id`, `database_id`.
7.  `cloudsql.googleapis.com/database/disk/read_ops_count`: Delta count of data
    disk read IO operations. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
8.  `cloudsql.googleapis.com/database/disk/write_ops_count`: Delta count of data
    disk write IO operations. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
9.  `cloudsql.googleapis.com/database/mysql/queries`: Delta count of statements
    executed by the server. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
10. `cloudsql.googleapis.com/database/mysql/questions`: Delta count of
    statements sent by the client. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
11. `cloudsql.googleapis.com/database/mysql/received_bytes_count`: Delta count
    of bytes received by MySQL process. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
12. `cloudsql.googleapis.com/database/mysql/sent_bytes_count`: Delta count of
    bytes sent by MySQL process. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
13. `cloudsql.googleapis.com/database/mysql/innodb_buffer_pool_pages_dirty`:
    Number of unflushed pages in the InnoDB buffer pool. `cloudsql_database`.
    `database`, `project_id`, `database_id`.
14. `cloudsql.googleapis.com/database/mysql/innodb_buffer_pool_pages_free`:
    Number of unused pages in the InnoDB buffer pool. `cloudsql_database`.
    `database`, `project_id`, `database_id`.
15. `cloudsql.googleapis.com/database/mysql/innodb_buffer_pool_pages_total`:
    Total number of pages in the InnoDB buffer pool. `cloudsql_database`.
    `database`, `project_id`, `database_id`.
16. `cloudsql.googleapis.com/database/mysql/innodb_data_fsyncs`: Delta count of
    InnoDB fsync() calls. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
17. `cloudsql.googleapis.com/database/mysql/innodb_os_log_fsyncs`: Delta count
    of InnoDB fsync() calls to the log file. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
18. `cloudsql.googleapis.com/database/mysql/innodb_pages_read`: Delta count of
    InnoDB pages read. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
19. `cloudsql.googleapis.com/database/mysql/innodb_pages_written`: Delta count
    of InnoDB pages written. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
20. `cloudsql.googleapis.com/database/mysql/open_tables`: The number of tables
    that are currently open. `cloudsql_database`. `database`, `project_id`,
    `database_id`.
21. `cloudsql.googleapis.com/database/mysql/opened_table_count`: The number of
    tables opened since the last sample. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
22. `cloudsql.googleapis.com/database/mysql/open_table_definitions`: The number
    of table definitions currently cached. `cloudsql_database`. `database`,
    `project_id`, `database_id`.
23. `cloudsql.googleapis.com/database/mysql/opened_table_definitions_count`: The
    number of table definitions cached since the last sample.
    `cloudsql_database`. `database`, `project_id`, `database_id`.
24. `cloudsql.googleapis.com/database/mysql/innodb/dictionary_memory`: Memory
    allocated for the InnoDB dictionary cache. `cloudsql_database`. `database`,
    `project_id`, `database_id`.

#### Parameters

Name      | Type   | Description                         | Required | Default
:-------- | :----- | :---------------------------------- | :------- | :------
projectId | string | The Id of the Google Cloud project. | Yes      |
query     | string | The promql query to execute.        | Yes      |

--------------------------------------------------------------------------------

### list_active_queries

Lists top N (default 10) ongoing queries from processlist and innodb_trx,
ordered by execution time in descending order. Returns detailed information of
those queries in json format, including process id, query, transaction duration,
transaction wait duration, process time, transaction state, process state,
username with host, transaction rows locked, transaction rows modified, and db
schema.

#### Parameters

| Name              | Type    | Description               | Required | Default |
| :---------------- | :------ | :------------------------ | :------- | :------ |
| min_duration_secs | integer | Optional: Only show       | No       | `0`     |
:                   :         : queries running for at    :          :         :
:                   :         : least this long in        :          :         :
:                   :         : seconds                   :          :         :
| limit             | integer | Optional: The maximum     | No       | `100`   |
:                   :         : number of rows to return. :          :         :

--------------------------------------------------------------------------------

### list_table_fragmentation

List table fragmentation in MySQL, by calculating the size of the data and index
files and free space allocated to each table. The query calculates fragmentation
percentage which represents the proportion of free space relative to the total
data and index size. Storage can be reclaimed for tables with high fragmentation
using OPTIMIZE TABLE.

#### Parameters

| Name                      | Type    | Description   | Required | Default |
| :------------------------ | :------ | :------------ | :------- | :------ |
| table_schema              | string  | (Optional)    | No       | ``      |
:                           :         : The database  :          :         :
:                           :         : where         :          :         :
:                           :         : fragmentation :          :         :
:                           :         : check is to   :          :         :
:                           :         : be executed.  :          :         :
:                           :         : Check all     :          :         :
:                           :         : tables        :          :         :
:                           :         : visible to    :          :         :
:                           :         : the current   :          :         :
:                           :         : user if not   :          :         :
:                           :         : specified     :          :         :
| table_name                | string  | (Optional)    | No       | ``      |
:                           :         : Name of the   :          :         :
:                           :         : table to be   :          :         :
:                           :         : checked.      :          :         :
:                           :         : Check all     :          :         :
:                           :         : tables        :          :         :
:                           :         : visible to    :          :         :
:                           :         : the current   :          :         :
:                           :         : user if not   :          :         :
:                           :         : specified.    :          :         :
| data_free_threshold_bytes | integer | (Optional)    | No       | `1`     |
:                           :         : Only show     :          :         :
:                           :         : tables with   :          :         :
:                           :         : at least this :          :         :
:                           :         : much free     :          :         :
:                           :         : space in      :          :         :
:                           :         : bytes.        :          :         :
:                           :         : Default is 1  :          :         :
| limit                     | integer | (Optional)    | No       | `10`    |
:                           :         : Max rows to   :          :         :
:                           :         : return,       :          :         :
:                           :         : default is 10 :          :         :

--------------------------------------------------------------------------------

### list_table_stats

Display table statistics including table size, total latency, rows read, rows
written, read and write latency for entire instance, a specified database, or a
specified table. Specifying a database name or table name filters the output to
that specific db or table. Results are limited to 10 by default.

#### Parameters

| Name             | Type    | Description                | Required | Default |
| :--------------- | :------ | :------------------------- | :------- | :------ |
| table_schema     | string  | (Optional) The database    | No       | ``      |
:                  :         : where statistics is to be  :          :         :
:                  :         : executed. Check all tables :          :         :
:                  :         : visible to the current     :          :         :
:                  :         : user if not specified      :          :         :
| table_name       | string  | (Optional) Name of the     | No       | ``      |
:                  :         : table to be checked. Check :          :         :
:                  :         : all tables visible to the  :          :         :
:                  :         : current user if not        :          :         :
:                  :         : specified.                 :          :         :
| sort_by          | string  | (Optional) The column to   | No       | ``      |
:                  :         : sort by                    :          :         :
| limit            | integer | (Optional) Max rows to     | No       | `10`    |
:                  :         : return, default is 10      :          :         :
| connected_schema | string  | (Optional) The connected   | No       |         |
:                  :         : db                         :          :         :

--------------------------------------------------------------------------------

### list_tables_missing_unique_indexes

Find tables that do not have primary or unique key constraint. A primary key or
unique key is the only mechanism that guaranttes a row is unique. Without them,
the database-level protection against data integrity issues will be missing.

#### Parameters

| Name         | Type    | Description                    | Required | Default |
| :----------- | :------ | :----------------------------- | :------- | :------ |
| table_schema | string  | (Optional) The database where  | No       | ``      |
:              :         : the check is to be performed.  :          :         :
:              :         : Check all tables visible to    :          :         :
:              :         : the current user if not        :          :         :
:              :         : specified                      :          :         :
| limit        | integer | (Optional) Max rows to return, | No       | `50`    |
:              :         : default is 50                  :          :         :

--------------------------------------------------------------------------------
