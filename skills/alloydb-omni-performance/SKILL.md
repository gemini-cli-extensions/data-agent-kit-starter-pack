---
name: alloydb-omni-performance
description: Use these skills when you need to analyze query performance, generate execution plans, check table/column statistics, and monitor overall database activity.
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

### execute_sql

Use this skill to execute a single SQL statement.

#### Parameters

Name | Type   | Description         | Required | Default
:--- | :----- | :------------------ | :------- | :------
sql  | string | The sql to execute. | Yes      |

--------------------------------------------------------------------------------

### get_column_cardinality

Estimates the number of unique values (cardinality) quickly for one or all
columns in a specific PostgreSQL table by using the database's internal
statistics, returning the results in descending order of estimated cardinality.
Please run ANALYZE on the table before using this skill to get accurate results.
The skill returns the column_name and the estimated_cardinality. If the
column_name is not provided, the skill returns all columns along with their
estimated cardinality.

#### Parameters

| Name        | Type   | Description                    | Required | Default  |
| :---------- | :----- | :----------------------------- | :------- | :------- |
| schema_name | string | Optional: The schema name in   | No       | `public` |
:             :        : which the table is present.    :          :          :
| table_name  | string | Required: The table name in    | Yes      |          |
:             :        : which the column is present.   :          :          :
| column_name | string | Optional: The column name for  | No       |          |
:             :        : which the cardinality is to be :          :          :
:             :        : found. If not provided,        :          :          :
:             :        : cardinality for all columns    :          :          :
:             :        : will be returned.              :          :          :

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
| exclude_application_names | string  | Optional: A     | No       |         |
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
| database_name      | string  | Optional: A specific     | No       |         |
:                    :         : database name pattern to :          :         :
:                    :         : search for.              :          :         :
| include_templates  | boolean | Optional: Whether to     | No       | `false` |
:                    :         : include template         :          :         :
:                    :         : databases in the         :          :         :
:                    :         : results.                 :          :         :
| database_owner     | string  | Optional: A specific     | No       |         |
:                    :         : database owner name      :          :         :
:                    :         : pattern to search for.   :          :         :
| default_tablespace | string  | Optional: A specific     | No       |         |
:                    :         : default tablespace name  :          :         :
:                    :         : pattern to search for.   :          :         :
| order_by           | string  | Optional: The field to   | No       |         |
:                    :         : order the results by.    :          :         :
:                    :         : Valid values are 'size'  :          :         :
:                    :         : and 'commit'.            :          :         :
| limit              | integer | Optional: The maximum    | No       | `10`    |
:                    :         : number of rows to        :          :         :
:                    :         : return.                  :          :         :

--------------------------------------------------------------------------------

### list_query_stats

Lists performance statistics for executed queries ordered by total time,
filtering by database name pattern if provided. This skill requires the
pg_stat_statements extension to be installed. The skill returns the database
name, query text, execution count, timing metrics (total, min, max, mean), rows
affected, and buffer cache I/O statistics (hits and reads).

#### Parameters

| Name          | Type    | Description                  | Required | Default |
| :------------ | :------ | :--------------------------- | :------- | :------ |
| database_name | string  | Optional: The database name  | No       |         |
:               :         : to list query stats for.     :          :         :
| limit         | integer | Optional: The maximum number | No       | `50`    |
:               :         : of results to return.        :          :         :
:               :         : Defaults to 50.              :          :         :

--------------------------------------------------------------------------------

### list_table_stats

Lists the user table statistics in the database ordered by number of sequential
scans with a default limit of 50 rows. Returns the following columns: schema
name, table name, table size in bytes, number of sequential scans, number of
index scans, idx_scan_ratio_percent (showing the percentage of total scans that
utilized an index, where a low ratio indicates missing or ineffective indexes),
number of live rows, number of dead rows, dead_row_ratio_percent (indicating
potential table bloat), total number of rows inserted, updated, and deleted, the
timestamps for the last_vacuum, last_autovacuum, and last_autoanalyze
operations.

#### Parameters

| Name        | Type    | Description                   | Required | Default  |
| :---------- | :------ | :---------------------------- | :------- | :------- |
| schema_name | string  | Optional: A specific schema   | No       | `public` |
:             :         : name to filter by             :          :          :
| table_name  | string  | Optional: A specific table    | No       |          |
:             :         : name to filter by             :          :          :
| owner       | string  | Optional: A specific owner to | No       |          |
:             :         : filter by                     :          :          :
| sort_by     | string  | Optional: The column to sort  | No       |          |
:             :         : by                            :          :          :
| limit       | integer | Optional: The maximum number  | No       | `50`     |
:             :         : of results to return          :          :          :

--------------------------------------------------------------------------------
