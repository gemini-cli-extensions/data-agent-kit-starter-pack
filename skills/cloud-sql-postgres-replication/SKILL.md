---
name: cloud-sql-postgres-replication
description: Use these skills when you need to monitor replication health, manage sync states between nodes, and audit database roles and security settings to ensure environment integrity.
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

### list_publication_tables

#### Parameters

| Name              | Type    | Description     | Required | Default |
| :---------------- | :------ | :-------------- | :------- | :------ |
| table_names       | string  | Optional:       | No       | ``      |
:                   :         : Filters by a    :          :         :
:                   :         : comma-separated :          :         :
:                   :         : list of table   :          :         :
:                   :         : names.          :          :         :
| publication_names | string  | Optional:       | No       | ``      |
:                   :         : Filters by a    :          :         :
:                   :         : comma-separated :          :         :
:                   :         : list of         :          :         :
:                   :         : publication     :          :         :
:                   :         : names.          :          :         :
| schema_names      | string  | Optional:       | No       | ``      |
:                   :         : Filters by a    :          :         :
:                   :         : comma-separated :          :         :
:                   :         : list of schema  :          :         :
:                   :         : names.          :          :         :
| limit             | integer | Optional: The   | No       | `50`    |
:                   :         : maximum number  :          :         :
:                   :         : of rows to      :          :         :
:                   :         : return.         :          :         :

--------------------------------------------------------------------------------

### list_replication_slots

List key details for all PostgreSQL replication slots (e.g., type, database,
active status) and calculates the size of the outstanding WAL that is being
prevented from removal by the slot.

--------------------------------------------------------------------------------

### list_roles

Lists all the user-created roles in the instance . It returns the role name,
Object ID, the maximum number of concurrent connections the role can make, along
with boolean indicators for: superuser status, privilege inheritance from member
roles, ability to create roles, ability to create databases, ability to log in,
replication privilege, and the ability to bypass row-level security, the
password expiration timestamp, a list of direct members belonging to this role,
and a list of other roles/groups that this role is a member of.

#### Parameters

| Name      | Type    | Description                     | Required | Default |
| :-------- | :------ | :------------------------------ | :------- | :------ |
| role_name | string  | Optional: a text to filter      | No       | ``      |
:           :         : results by role name. The input :          :         :
:           :         : is used within a LIKE clause.   :          :         :
| limit     | integer | Optional: The maximum number of | No       | `50`    |
:           :         : rows to return. Default is 10   :          :         :

--------------------------------------------------------------------------------

### replication_stats

Lists each replica's process ID, user name, application name, backend_xmin
(standby's xmin horizon reported by hot_standby_feedback), client IP address,
connection state, and sync_state, along with lag sizes in bytes for sent_lag
(primary to sent), write_lag (sent to written), flush_lag (written to flushed),
replay_lag (flushed to replayed), and the overall total_lag (primary to
replayed).

--------------------------------------------------------------------------------
