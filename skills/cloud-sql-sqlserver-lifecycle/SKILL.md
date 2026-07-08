---
name: cloud-sql-sqlserver-lifecycle
description: Use these skills when you need to manage the lifecycle and durability of your data, including creating backups, restoring from existing backups, and cloning instances for testing or migration.
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

### clone_instance

Clone an existing Cloud SQL instance into a new instance. The clone can be a
direct copy of the source instance, or a point-in-time-recovery (PITR) clone
from a specific timestamp. The call returns a Cloud SQL Operation object. Call
wait_for_operation tool after this, make sure to use multiplier as 4 to poll the
opertation status till it is marked DONE.

#### Parameters

| Name                    | Type   | Description     | Required | Default |
| :---------------------- | :----- | :-------------- | :------- | :------ |
| project                 | string | The GCP project | No       |         |
:                         :        : ID. This is     :          :         :
:                         :        : pre-configured; :          :         :
:                         :        : do not ask for  :          :         :
:                         :        : it unless the   :          :         :
:                         :        : user explicitly :          :         :
:                         :        : provides a      :          :         :
:                         :        : different one.  :          :         :
| sourceInstanceName      | string | The name of the | Yes      |         |
:                         :        : instance to be  :          :         :
:                         :        : cloned.         :          :         :
| destinationInstanceName | string | The name of the | Yes      |         |
:                         :        : new instance    :          :         :
:                         :        : that will be    :          :         :
:                         :        : created by      :          :         :
:                         :        : cloning the     :          :         :
:                         :        : source          :          :         :
:                         :        : instance.       :          :         :
| pointInTime             | string | The timestamp   | No       |         |
:                         :        : in RFC 3339     :          :         :
:                         :        : format to which :          :         :
:                         :        : the source      :          :         :
:                         :        : instance should :          :         :
:                         :        : be cloned.      :          :         :
| preferredZone           | string | The preferred   | No       |         |
:                         :        : zone for the    :          :         :
:                         :        : new instance.   :          :         :
| preferredSecondaryZone  | string | The preferred   | No       |         |
:                         :        : secondary zone  :          :         :
:                         :        : for the new     :          :         :
:                         :        : instance.       :          :         :

--------------------------------------------------------------------------------

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
