---
name: spanner-data
description: Use these skills when you need to explore the database structure, discover schema objects like tables and graphs, and execute custom SQL queries to interact with your data.
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


### execute_sql

Use this tool to execute DML SQL. Please use the googlesql interface for Spanner.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| sql | string | The sql to execute. | Yes |  |


---

### execute_sql_dql

Use this tool to execute DQL SQL. Please use the googlesql interface for Spanner.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| sql | string | The sql to execute. | Yes |  |


---

### list_graphs

Lists detailed graph schema information (node tables, edge tables, labels and property declarations) as JSON for user-created graphs. Filters by a comma-separated list of graph names. If names are omitted, lists all graphs. The output can be 'simple' (graph names only) or 'detailed' (full schema).

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| graph_names | string | Optional: A comma-separated list of graph names. If empty, details for all graphs in user-accessible schemas will be listed. | No | `` |
| output_format | string | Optional: Use 'simple' to return graph names only or use 'detailed' to return the full information schema. | No | `detailed` |


---

### list_tables

Lists detailed schema information (object type, columns, constraints, indexes) as JSON for user-created tables (ordinary or partitioned). Filters by a comma-separated list of names. If names are omitted, lists all tables in user schemas. The output can be 'simple' (table names only) or 'detailed' (full schema).

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| table_names | string | Optional: A comma-separated list of table names. If empty, details for all tables in user-accessible schemas will be listed. | No | `` |
| output_format | string | Optional: Use 'simple' to return table names only or use 'detailed' to return the full information schema. | No | `detailed` |


---

