# Direct Inspection of Table Schema

> [!IMPORTANT] When resource names (project, instance, database, table) are
> specified in the prompt or task: 1. **Call tools and CLI commands with full
> required scoping arguments** (`instance_id`, `database_id`, `project_id`). 2.
> **Check for parameter errors**: If a tool returns `INVALID_ARGUMENT`, verify
> and correct your arguments before switching tools. 3. **Scanning through
> instances is allowed as a fallback** when resource names are not specified or
> a verified direct check returns `NOT_FOUND`. Prior to scanning, you MUST
> attempt direct verification using the provided parameters.

## Single-Shot CLI Commands to Explore Schemas

### 1. Cloud Spanner Tables

To inspect the schema/DDL of a specific Spanner database:

```bash
gcloud spanner databases ddl describe <DATABASE_ID> \
    --instance=<INSTANCE_ID> \
    --project=<PROJECT_ID>
```

*Note:* This returns the complete DDL including table column names, types, and
primary keys in a single command.

### 2. BigQuery & BigLake Tables

To inspect BigQuery or BigLake table schemas:

```bash
bq show --schema --format=prettyjson <PROJECT_ID>:<DATASET_ID>.<TABLE_NAME>
```

Or query column metadata:

```bash
bq query --project_id=<PROJECT_ID> --use_legacy_sql=false \
    "SELECT column_name, data_type FROM \`<PROJECT_ID>.<DATASET_ID>.INFORMATION_SCHEMA.COLUMNS\` WHERE table_name = '<TABLE_NAME>'"
```

### 3. Cloud SQL (PostgreSQL / MySQL)

To inspect Cloud SQL instance details and connectivity (e.g., IP address,
region):

```bash
gcloud sql instances describe <INSTANCE_ID> --project=<PROJECT_ID>
```

*Note:* In PySpark, calling `spark.read.format("jdbc").option("url",
...).option("dbtable", ...).load()` automatically resolves the table schema from
the database metadata upon connection.

### 4. GCS Files (CSV / Parquet / Folder)

-   **CSV header inspection**:

    ```bash
    gcloud storage cat gs://<BUCKET>/<PATH>/file.csv | head -n 1
    ```

-   **Folder exploration**:

    ```bash
    gcloud storage ls gs://<BUCKET>/<PATH>/
    ```

--------------------------------------------------------------------------------

## When to Scan Instances (Fallback Only)

-   **Direct verification first**: If instance/database names are provided in
    the task, verify that specific resource directly.
-   **Scanning is permitted**: If the resource is genuinely not specified in the
    prompt, or if the direct check returns a verified `NOT_FOUND` (404),
    scanning instances within the project is allowed.
-   **Project scoping**: Do NOT scan across unrelated projects when the target
    project ID is already provided.
