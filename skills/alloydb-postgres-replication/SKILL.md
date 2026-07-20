---
name: alloydb-postgres-replication
description: Use these skills when you need to monitor replication health, manage sync states between nodes, and ensure the high availability and data distribution of your AlloyDB cluster.
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


### database_overview

Fetches the current state of the PostgreSQL server, returning the version, whether it's a replica, uptime duration, maximum connection limit, number of current connections, number of active connections, and the percentage of connections in use.



---

### get_instance

Retrieves details about a specific AlloyDB instance.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| project | string | The GCP project ID. This is pre-configured; do not ask for it unless the user explicitly provides a different one. | No |  |
| location | string | The location of the instance (e.g., 'us-central1'). | Yes |  |
| cluster | string | The ID of the cluster. | Yes |  |
| instance | string | The ID of the instance. | Yes |  |


---

### list_instances

Lists all AlloyDB instances in a given project, location and cluster.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| project | string | The GCP project ID. This is pre-configured; do not ask for it unless the user explicitly provides a different one. | No |  |
| location | string | Optional: The location of the cluster (e.g., 'us-central1'). Use '-' to get results for all regions.(Default: '-') | No | `-` |
| cluster | string | Optional: The ID of the cluster to list instances from. Use '-' to get results for all clusters.(Default: '-') | No | `-` |


---

### list_publication_tables



#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| table_names | string | Optional: Filters by a comma-separated list of table names. | No | `` |
| publication_names | string | Optional: Filters by a comma-separated list of publication names. | No | `` |
| schema_names | string | Optional: Filters by a comma-separated list of schema names. | No | `` |
| limit | integer | Optional: The maximum number of rows to return. | No | `50` |


---

### list_replication_slots

List key details for all PostgreSQL replication slots (e.g., type, database, active status) and calculates the size of the outstanding WAL that is being prevented from removal by the slot.



---

### replication_stats

Lists each replica's process ID, user name, application name, backend_xmin (standby's xmin horizon reported by hot_standby_feedback), client IP address, connection state, and sync_state, along with lag sizes in bytes for sent_lag (primary to sent), write_lag (sent to written), flush_lag (written to flushed), replay_lag (flushed to replayed), and the overall total_lag (primary to replayed).



---

