# Direct Inspection of table schema
[!CAUTION] Proceed with direct inspection ONLY if you have all the details.

## For BigQuery, Spanner and BigLake Icerberg tables and views
Use `gcp-data-assets-discovery` skill to find and lookup schema.

## For csv files
Peek first row of csv files

### For GCS files
Use `gcloud storage cat gs://bucket/file.csv | head -n 1`

### For local files
Use `head -n 1 file.csv`