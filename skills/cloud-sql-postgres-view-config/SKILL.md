---
name: cloud-sql-postgres-view-config
description: Use these skills when you need to discover and manage PostgreSQL extensions or fine-tune engine-level settings such as memory allocation and server configuration parameters.
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

### get_instance

#### Parameters

| Name       | Type   | Description     | Required | Default |
| :--------- | :----- | :-------------- | :------- | :------ |
| projectId  | string | The GCP project | No       |         |
:            :        : ID. This is     :          :         :
:            :        : pre-configured; :          :         :
:            :        : do not ask for  :          :         :
:            :        : it unless the   :          :         :
:            :        : user explicitly :          :         :
:            :        : provides a      :          :         :
:            :        : different one.  :          :         :
| instanceId | string | The instance ID | Yes      |         |

--------------------------------------------------------------------------------

### list_available_extensions

Discover all PostgreSQL extensions available for installation on this server,
returning name, default_version, and description.

--------------------------------------------------------------------------------

### list_installed_extensions

List all installed PostgreSQL extensions with their name, version, schema,
owner, and description.

--------------------------------------------------------------------------------

### list_memory_configurations

List PostgreSQL memory-related configurations (name and current setting) from
pg_settings.

--------------------------------------------------------------------------------

### list_pg_settings

#### Parameters

| Name         | Type    | Description   | Required | Default |
| :----------- | :------ | :------------ | :------- | :------ |
| setting_name | string  | Optional: A   | No       | ``      |
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
