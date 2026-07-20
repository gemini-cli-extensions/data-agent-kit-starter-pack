---
name: cloud-sql-mysql-data
description: Use these skills when you need to explore your database schema, execute SQL queries to interact with your data, and inspect how MySQL plans to execute your statements.
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

Use this skill to execute SQL.

#### Parameters

Name | Type   | Description         | Required | Default
:--- | :----- | :------------------ | :------- | :------
sql  | string | The sql to execute. | Yes      |

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

### list_tables

Lists detailed schema information (object type, columns, constraints, indexes,
triggers, comment) as JSON for user-created tables (ordinary or partitioned).
Filters by a comma-separated list of names. If names are omitted, lists all
tables in user schemas.

#### Parameters

| Name          | Type   | Description     | Required | Default    |
| :------------ | :----- | :-------------- | :------- | :--------- |
| table_names   | string | Optional: A     | No       | ``         |
:               :        : comma-separated :          :            :
:               :        : list of table   :          :            :
:               :        : names. If       :          :            :
:               :        : empty, details  :          :            :
:               :        : for all tables  :          :            :
:               :        : will be listed. :          :            :
| output_format | string | Optional: Use   | No       | `detailed` |
:               :        : 'simple' for    :          :            :
:               :        : names only or   :          :            :
:               :        : 'detailed' for  :          :            :
:               :        : full info.      :          :            :

--------------------------------------------------------------------------------
