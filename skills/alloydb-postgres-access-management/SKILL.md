---
name: alloydb-postgres-access-management
description: Use these skills when you need to manage database users, inspect permissions and roles, and verify global configuration parameters related to security and access control.
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


### create_user

Creates a new AlloyDB user within a cluster. Takes the new user's name and a secure password. Optionally, a list of database roles can be assigned. Always ask the user for the type of user to create. ALLOYDB_IAM_USER is recommended.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| project | string | The GCP project ID. This is pre-configured; do not ask for it unless the user explicitly provides a different one. | No |  |
| location | string | The location of the cluster (e.g., 'us-central1'). | Yes |  |
| cluster | string | The ID of the cluster where the user will be created. | Yes |  |
| user | string | The name for the new user. Must be unique within the cluster. | Yes |  |
| password | string | A secure password for the new user. Required only for ALLOYDB_BUILT_IN userType. | No |  |
| databaseRoles | array | Optional. A list of database roles to grant to the new user (e.g., ['pg_read_all_data']). | No | `[]` |
| userType | string | The type of user to create. Valid values are: ALLOYDB_BUILT_IN and ALLOYDB_IAM_USER. ALLOYDB_IAM_USER is recommended. | Yes |  |


---

### database_overview

Fetches the current state of the PostgreSQL server, returning the version, whether it's a replica, uptime duration, maximum connection limit, number of current connections, number of active connections, and the percentage of connections in use.



---

### get_user

Retrieves details about a specific AlloyDB user.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| project | string | The GCP project ID. This is pre-configured; do not ask for it unless the user explicitly provides a different one. | No |  |
| location | string | The location of the cluster (e.g., 'us-central1'). | Yes |  |
| cluster | string | The ID of the cluster. | Yes |  |
| user | string | The ID of the user. | Yes |  |


---

### list_pg_settings



#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| setting_name | string | Optional: A specific configuration parameter name pattern to search for. | No | `` |
| limit | integer | Optional: The maximum number of rows to return. | No | `50` |


---

### list_roles

Lists all the user-created roles in the instance . It returns the role name, Object ID, the maximum number of concurrent connections the role can make, along with boolean indicators for: superuser status, privilege inheritance from member roles, ability to create roles, ability to create databases, ability to log in, replication privilege, and the ability to bypass row-level security, the password expiration timestamp, a list of direct members belonging to this role, and a list of other roles/groups that this role is a member of.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| role_name | string | Optional: a text to filter results by role name. The input is used within a LIKE clause. | No | `` |
| limit | integer | Optional: The maximum number of rows to return. Default is 10 | No | `50` |


---

### list_users

Lists all AlloyDB users in a given project, location and cluster.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| project | string | The GCP project ID. This is pre-configured; do not ask for it unless the user explicitly provides a different one. | No |  |
| location | string | The location of the cluster (e.g., 'us-central1'). | Yes |  |
| cluster | string | The ID of the cluster to list users from. | Yes |  |


---

