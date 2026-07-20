---
name: alloydb-omni-health
description: Use these skills when you need to audit database health, identify storage bloat, find broken indexes, and verify tablespace or maintenance configurations.
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

### database_overview

Fetches the current state of the PostgreSQL server, returning the version,
whether it's a replica, uptime duration, maximum connection limit, number of
current connections, number of active connections, and the percentage of
connections in use.

--------------------------------------------------------------------------------

### list_autovacuum_configurations

List PostgreSQL autovacuum-related configurations (name and current setting)
from pg_settings.

--------------------------------------------------------------------------------

### list_invalid_indexes

Lists all invalid PostgreSQL indexes which are taking up disk space but are
unusable by the query planner. Typically created by failed CREATE INDEX
CONCURRENTLY operations.

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

### list_tablespaces

#### Parameters

| Name            | Type    | Description                 | Required | Default |
| :-------------- | :------ | :-------------------------- | :------- | :------ |
| tablespace_name | string  | Optional: a text to filter  | No       |         |
:                 :         : results by tablespace name. :          :         :
:                 :         : The input is used within a  :          :         :
:                 :         : LIKE clause.                :          :         :
| limit           | integer | Optional: The maximum       | No       | `50`    |
:                 :         : number of rows to return.   :          :         :

--------------------------------------------------------------------------------

### list_top_bloated_tables

List the top tables by dead-tuple (approximate bloat signal), returning schema,
table, live/dead tuples, percentage, and last vacuum/analyze times.

#### Parameters

Name  | Type    | Description                              | Required | Default
:---- | :------ | :--------------------------------------- | :------- | :------
limit | integer | The maximum number of results to return. | No       | `50`

--------------------------------------------------------------------------------
