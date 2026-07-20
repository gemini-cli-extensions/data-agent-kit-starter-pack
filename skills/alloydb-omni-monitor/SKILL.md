---
name: alloydb-omni-monitor
description: Use these skills when you need to troubleshoot production issues by identifying locks, tracking long-running transactions, and getting a high-level view of server state.
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

### list_locks

Identifies all locks held by active processes showing the process ID, user,
query text, and an aggregated list of all transactions and specific locks
(relation, mode, grant status) associated with each process.

--------------------------------------------------------------------------------

### list_pg_settings

#### Parameters

| Name         | Type    | Description   | Required | Default |
| :----------- | :------ | :------------ | :------- | :------ |
| setting_name | string  | Optional: A   | No       |         |
:              :         : specific      :          :         :
:              :         : configuration :          :         :
:              :         : parameter     :          :         :
:              :         : name pattern  :          :         :
:              :         : to search     :          :         :
:              :         : for.          :          :         :
| limit        | integer | Optional: The | No       | `50`    |
:              :         : maximum       :          :         :
:              :         : number of     :          :         :
:              :         : rows to       :          :         :
:              :         : return.       :          :         :

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
