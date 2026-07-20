---
name: alloydb-omni-optimize
description: Use these skills when you need to fine-tune the database engine settings, manage extensions, or optimize the columnar engine for better analytical performance.
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

### list_autovacuum_configurations

List PostgreSQL autovacuum-related configurations (name and current setting)
from pg_settings.

--------------------------------------------------------------------------------

### list_available_extensions

Discover all PostgreSQL extensions available for installation on this server,
returning name, default_version, and description.

--------------------------------------------------------------------------------

### list_columnar_configurations

List AlloyDB Omni columnar-related configurations (name and current setting)
from pg_settings.

--------------------------------------------------------------------------------

### list_columnar_recommended_columns

Lists columns that AlloyDB Omni recommends adding to the columnar engine to
improve query performance.

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
