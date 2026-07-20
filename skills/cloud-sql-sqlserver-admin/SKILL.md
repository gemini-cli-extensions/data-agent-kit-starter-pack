---
name: cloud-sql-sqlserver-admin
description: Use these skills when you need to provision new Cloud SQL for SQL Server instances, create databases and users, clone existing environments, and monitor the progress of long-running operations.
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

### create_database

#### Parameters

| Name     | Type   | Description     | Required | Default |
| :------- | :----- | :-------------- | :------- | :------ |
| project  | string | The GCP project | No       |         |
:          :        : ID. This is     :          :         :
:          :        : pre-configured; :          :         :
:          :        : do not ask for  :          :         :
:          :        : it unless the   :          :         :
:          :        : user explicitly :          :         :
:          :        : provides a      :          :         :
:          :        : different one.  :          :         :
| instance | string | The ID of the   | Yes      |         |
:          :        : instance where  :          :         :
:          :        : the database    :          :         :
:          :        : will be         :          :         :
:          :        : created.        :          :         :
| name     | string | The name for    | Yes      |         |
:          :        : the new         :          :         :
:          :        : database. Must  :          :         :
:          :        : be unique       :          :         :
:          :        : within the      :          :         :
:          :        : instance.       :          :         :

--------------------------------------------------------------------------------

### create_instance

#### Parameters

Name            | Type   | Description                                                                                                                                              | Required | Default
:-------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------
project         | string | The GCP project ID. This is pre-configured; do not ask for it unless the user explicitly provides a different one.                                       | No       |
name            | string | The name of the instance                                                                                                                                 | Yes      |
databaseVersion | string | The database version for SQL Server. If not specified, defaults to SQLSERVER_2022_STANDARD.                                                              | No       | `SQLSERVER_2022_STANDARD`
rootPassword    | string | The root password for the instance                                                                                                                       | Yes      |
editionPreset   | string | The edition of the instance. Can be `Production` or `Development`. This determines the default machine type and availability. Defaults to `Development`. | No       | `Development`

--------------------------------------------------------------------------------

### create_user

#### Parameters

| Name     | Type    | Description     | Required | Default |
| :------- | :------ | :-------------- | :------- | :------ |
| project  | string  | The GCP project | No       |         |
:          :         : ID. This is     :          :         :
:          :         : pre-configured; :          :         :
:          :         : do not ask for  :          :         :
:          :         : it unless the   :          :         :
:          :         : user explicitly :          :         :
:          :         : provides a      :          :         :
:          :         : different one.  :          :         :
| instance | string  | The ID of the   | Yes      |         |
:          :         : instance where  :          :         :
:          :         : the user will   :          :         :
:          :         : be created.     :          :         :
| name     | string  | The name for    | Yes      |         |
:          :         : the new user.   :          :         :
:          :         : Must be unique  :          :         :
:          :         : within the      :          :         :
:          :         : instance.       :          :         :
| password | string  | A secure        | No       |         |
:          :         : password for    :          :         :
:          :         : the new user.   :          :         :
:          :         : Not required    :          :         :
:          :         : for IAM users.  :          :         :
| iamUser  | boolean | Set to true to  | Yes      |         |
:          :         : create a Cloud  :          :         :
:          :         : IAM user.       :          :         :

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

### list_databases

Lists all databases for a Cloud SQL instance.

#### Parameters

| Name     | Type   | Description     | Required | Default |
| :------- | :----- | :-------------- | :------- | :------ |
| project  | string | The GCP project | No       |         |
:          :        : ID. This is     :          :         :
:          :        : pre-configured; :          :         :
:          :        : do not ask for  :          :         :
:          :        : it unless the   :          :         :
:          :        : user explicitly :          :         :
:          :        : provides a      :          :         :
:          :        : different one.  :          :         :
| instance | string | The instance ID | Yes      |         |

--------------------------------------------------------------------------------

### list_instances

Lists all type of Cloud SQL instances for a project.

#### Parameters

| Name    | Type   | Description     | Required | Default |
| :------ | :----- | :-------------- | :------- | :------ |
| project | string | The GCP project | No       |         |
:         :        : ID. This is     :          :         :
:         :        : pre-configured; :          :         :
:         :        : do not ask for  :          :         :
:         :        : it unless the   :          :         :
:         :        : user explicitly :          :         :
:         :        : provides a      :          :         :
:         :        : different one.  :          :         :

--------------------------------------------------------------------------------

### wait_for_operation

#### Parameters

| Name      | Type   | Description     | Required | Default |
| :-------- | :----- | :-------------- | :------- | :------ |
| project   | string | The GCP project | No       |         |
:           :        : ID. This is     :          :         :
:           :        : pre-configured; :          :         :
:           :        : do not ask for  :          :         :
:           :        : it unless the   :          :         :
:           :        : user explicitly :          :         :
:           :        : provides a      :          :         :
:           :        : different one.  :          :         :
| operation | string | The operation   | Yes      |         |
:           :        : ID              :          :         :

--------------------------------------------------------------------------------
