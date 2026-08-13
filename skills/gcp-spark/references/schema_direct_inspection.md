# Direct Inspection of table schema

## For BigQuery, Spanner and BigLake Iceberg tables and views

Biglake tables are often specified in format `catalog.schema.table`, the first
segment is the **Catalog Name**, NOT a GCP project ID.

Use the following CLI commands for direct schema and table inspection:

### 1. Cloud Spanner

```sh
gcloud spanner databases ddl describe <DATABASE_ID> --instance=<INSTANCE_ID> --project=<PROJECT_ID>
```

### 2. BigQuery / BigLake

Direct schema and table inspection:

```bash
bq show --schema --format=prettyjson <TARGET_PROJECT>:<DATASET_ID>.<TABLE_NAME>
```

**Typo & Error Masking Handling**: On external or shared datasets, `bq show`,
`bq ls`, and `INFORMATION_SCHEMA.TABLES` often fail with `Access Denied` due to
lacking metadata list permissions on foreign projects. However, data querying
via `bq query` executes using your active billing project and succeeds on all
readable tables.

When a table read or `bq show` fails:

1.  **Test singular/plural and typo variants directly via `bq query`**: Test
    candidate table names directly with a 1-row query:

    ```bash
    bq query --use_legacy_sql=false "SELECT * FROM \`<TARGET_PROJECT>.<DATASET_ID>.<CANDIDATE_TABLE>\` LIMIT 1"
    ```

    *Example*: If `sqlgen-testing.financial.loans` fails, immediately test the
    singular form `loan`:

    ```bash
    bq query --use_legacy_sql=false "SELECT * FROM \`sqlgen-testing.financial.loan\` LIMIT 1"
    ```

    This command verifies table existence and directly outputs the column schema
    and values (e.g., `loan_id`, `account_id`, `date`, `amount`, `duration`,
    `payments`, `status`) in the query result.

2.  **Autonomous minor typo fix**: Autonomously fix the typo within the target
    dataset (`sqlgen-testing.financial.loan`) in PySpark:

    ```python
    df = (
        spark.read.format("bigquery")
        .option("table", "sqlgen-testing.financial.loan")
        .load()
    )
    ```

    Proceed immediately with notebook creation and execution using the corrected
    table name (`loan`) without stopping or asking the user. NEVER revert back
    to the misspelled table name (`loans`) in the notebook code or markdown
    cells, even if direct CLI queries return permission or environment errors in
    test sandboxes.

3.  **Strict Project Isolation**: NEVER call `bigquery__search_catalog` to
    search across other GCP projects and NEVER substitute tables from local or
    unrelated projects (e.g. do NOT switch to `datagravity-demo` or
    `cloud-db-nl2sql` when the user requested `sqlgen-testing`).

### 3. Cloud SQL (PostgreSQL / MySQL)

```bash
gcloud sql instances describe <INSTANCE_ID> --project=<PROJECT_ID>
```

## For GCS bucket or folder exploration

If the user specifies a GCS bucket or folder instead of specific files, you
**MUST** explore the folder contents first to identify relevant files using
`gcloud storage ls gs://<GCS_BUCKET>/<PATH>` command.

## For CSV file

Peek first row of CSV file

### For CSV file in GCS

Use `gcloud storage cat gs://bucket/file.csv | head -n 1`

### For local CSV file
Use `head -n 1 file.csv`
