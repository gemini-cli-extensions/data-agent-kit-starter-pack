# Direct Inspection of table schema

## For BigQuery, Spanner and BigLake Iceberg tables and views
Use `@skill:discovering-gcp-data-assets` skill to find and lookup schema.

## For GCS bucket or folder exploration
If the user specifies a GCS bucket or folder instead of specific files, you
**MUST** explore the folder contents first to identify relevant files using
`gcloud storage ls gs://<GCS_BUCKET>/<PATH>`
command.

## For CSV file
Peek first row of CSV file

### For CSV file in GCS
Use `gcloud storage cat gs://bucket/file.csv | head -n 1`

### For local CSV file
Use `head -n 1 file.csv`