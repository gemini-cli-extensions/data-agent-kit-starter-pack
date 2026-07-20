---
name: cloud-sql-postgres-lifecycle
description: Use these skills when you need to manage the lifecycle of your instances, including performing backups and restores, checking major version upgrade compatibility, and monitoring overall instance status.
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

### create_backup

Creates a backup on a Cloud SQL instance.

#### Parameters

| Name               | Type   | Description     | Required | Default |
| :----------------- | :----- | :-------------- | :------- | :------ |
| project            | string | The GCP project | No       |         |
:                    :        : ID. This is     :          :         :
:                    :        : pre-configured; :          :         :
:                    :        : do not ask for  :          :         :
:                    :        : it unless the   :          :         :
:                    :        : user explicitly :          :         :
:                    :        : provides a      :          :         :
:                    :        : different one.  :          :         :
| instance           | string | Cloud SQL       | Yes      |         |
:                    :        : instance ID.    :          :         :
:                    :        : This does not   :          :         :
:                    :        : include the     :          :         :
:                    :        : project ID.     :          :         :
| location           | string | Location of the | No       |         |
:                    :        : backup run.     :          :         :
| backup_description | string | The description | No       |         |
:                    :        : of this backup  :          :         :
:                    :        : run.            :          :         :

--------------------------------------------------------------------------------

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

### postgres_upgrade_precheck

Analyzes a Cloud SQL PostgreSQL instance for major version upgrade readiness.
Results are provided to guide customer actions: ERROR: Action Required. These
are critical issues blocking the upgrade. Customers must resolve these using the
provided actions_required steps before attempting the upgrade. WARNING: Review
Recommended. These are potential issues. Customers should review the message and
actions_required. While not blocking, addressing these is advised to prevent
future problems or unexpected behavior post-upgrade. INFO: No Action Needed.
Informational messages only. This pre-check helps customers proactively fix
problems, preventing upgrade failures and ensuring a smoother transition.

#### Parameters

| Name                  | Type   | Description    | Required | Default       |
| :-------------------- | :----- | :------------- | :------- | :------------ |
| project               | string | The project ID | Yes      |               |
| instance              | string | The name of    | Yes      |               |
:                       :        : the instance   :          :               :
:                       :        : to check       :          :               :
| targetDatabaseVersion | string | The target     | No       | `POSTGRES_18` |
:                       :        : PostgreSQL     :          :               :
:                       :        : version for    :          :               :
:                       :        : the upgrade    :          :               :
:                       :        : (e.g.,         :          :               :
:                       :        : POSTGRES_18).  :          :               :
:                       :        : If not         :          :               :
:                       :        : specified,     :          :               :
:                       :        : defaults to    :          :               :
:                       :        : the            :          :               :
:                       :        : PostgreSQL 18. :          :               :

--------------------------------------------------------------------------------

### restore_backup

Restores a backup on a Cloud SQL instance.

#### Parameters

| Name            | Type   | Description     | Required | Default |
| :-------------- | :----- | :-------------- | :------- | :------ |
| target_project  | string | The GCP project | No       |         |
:                 :        : ID. This is     :          :         :
:                 :        : pre-configured; :          :         :
:                 :        : do not ask for  :          :         :
:                 :        : it unless the   :          :         :
:                 :        : user explicitly :          :         :
:                 :        : provides a      :          :         :
:                 :        : different one.  :          :         :
| target_instance | string | Cloud SQL       | Yes      |         |
:                 :        : instance ID of  :          :         :
:                 :        : the target      :          :         :
:                 :        : instance. This  :          :         :
:                 :        : does not        :          :         :
:                 :        : include the     :          :         :
:                 :        : project ID.     :          :         :
| backup_id       | string | Identifier of   | Yes      |         |
:                 :        : the backup      :          :         :
:                 :        : being restored. :          :         :
:                 :        : Can be a        :          :         :
:                 :        : BackupRun ID,   :          :         :
:                 :        : backup name, or :          :         :
:                 :        : BackupDR backup :          :         :
:                 :        : name. Use the   :          :         :
:                 :        : full backup ID  :          :         :
:                 :        : as provided, do :          :         :
:                 :        : not try to      :          :         :
:                 :        : parse it        :          :         :
| source_project  | string | GCP project ID  | No       |         |
:                 :        : of the instance :          :         :
:                 :        : that the backup :          :         :
:                 :        : belongs to.     :          :         :
:                 :        : Only required   :          :         :
:                 :        : if the          :          :         :
:                 :        : backup_id is a  :          :         :
:                 :        : BackupRun ID.   :          :         :
| source_instance | string | Cloud SQL       | No       |         |
:                 :        : instance ID of  :          :         :
:                 :        : the instance    :          :         :
:                 :        : that the backup :          :         :
:                 :        : belongs to.     :          :         :
:                 :        : Only required   :          :         :
:                 :        : if the          :          :         :
:                 :        : backup_id is a  :          :         :
:                 :        : BackupRun ID.   :          :         :

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
