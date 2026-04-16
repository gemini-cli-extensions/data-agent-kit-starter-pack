---
name: discovering-gcp-data-assets
description: |
  Finds and inspects data assets within Google Cloud.
  Relevant when any of the following conditions are true:
    1. The user request involves finding, exploring, or inspecting data assets
       in Google Cloud, such as:
         - BigQuery datasets, tables, or views
         - BigLake catalog or tables
         - Spanner instances, databases or tables
         - etc.
    2. You need to retrieve the schema, metadata, or governance policies for a
       GCP data asset.
    3. You have a keyword or topic (e.g., "sales data") but lack the specific
       table or resource ID.
    4. You are attempting to find data using `bq ls`, as this skill offers a
       superior approach.
  Don't use when:
    - Assets are outside Google Cloud
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

# Instructions

## Step 1: Handle Public Datasets or Proceed to Search

Dataplex Entries Lookup provides the richest metadata for data assets. You MUST
prioritize using it for all Google Cloud assets, even if you already know their
IDs.

-   **Public Datasets (Direct Inspection)**: If the requested asset belongs to
    the `bigquery-public-data` project, Dataplex Entries Lookup will fail. You
    MUST skip Steps 2 and 3 and inspect the table directly using the `bq` CLI or
    BigQuery MCP tools instead.
-   **All Other Assets (Proceed to Step 2)**: For all other BigQuery, Cloud
    Storage, Spanner, BigLake Iceberg or general GCP data assets (whether their
    IDs are known or missing), you MUST proceed to **Step 2** to search the
    Dataplex catalog and obtain their full Entry Name.

## Step 2: Execute Discovery Search

You MUST use the Dataplex search command to discover assets and retrieve their
full `projects/...` entry names. This step is required even if you already know
the asset's short ID (e.g., `my_dataset.my_table`), because Step 3 strictly
requires the full entry name.

> [!IMPORTANT] The `--project` parameter MUST ALWAYS be provided. This
> project_id is used to attribute the search only and does NOT restrict the
> search scope. The project must have the dataplex API enabled and user must
> have the `dataplex.entries.get` permissions.

### A. Semantic Search (Natural Language Intent)

Use this when the user describes the **meaning** or **intent** of the data
(e.g., "Find Q4 product sales data").

Use the `search_entries` MCP tool

OR

```bash
gcloud dataplex entries search "<NATURAL_LANGUAGE_QUERY>" \
  --project="<PROJECT_ID>" \
  --semantic-search \
  --limit=50
```

### B. Keyword Search (Technical Strings)

Use this for exact keyword matches or technical strings (e.g., `name:order_v2`).

#### Search Query Rules (MANDATORY)

-   **Mode-Specific Syntax**:
    -   **Semantic Search**: Logical operators (`AND`, `OR`) MUST be
        **UPPERCASE**. Use plural `labels.` for label filters (e.g.,
        `labels.env=prod`).
    -   **Keyword Search**: Operators are case-insensitive. Use singular
        `label.` for label filters (e.g., `label.env=prod`).
-   **Abbreviated Logic**: Use `|` for OR and `,` for AND within parentheses to
    shorten queries (e.g., `projectid:(prod|staging)` or `column:(id,name)`).
-   **Exact vs. Token Match**:
    -   Use `:` for token/substring matches (e.g., `name:sales`).
    -   Use `=` for exact matches. REQUIRED for `system`, `type`, and
        `location`.
-   **Singular Keywords**: ALWAYS convert plurals to singular (e.g., "product"
    NOT "products").
-   **Scope Restriction**: You SHOULD restrict the search scope using a `parent`
    filter if the project or dataset is known (e.g.,
    `parent:projects/<PROJECT_ID>`).

#### Dataplex Search Syntax Reference

-   **`name:x`**: Substring/token match on resource ID.
-   **`displayname:x`**: Substring/token match on display name.
-   **`projectid:x`**: Substring/token match on GCP project ID.
-   **`parent:x`**: Substring match on hierarchical path (e.g.,
    `projects/my-proj`).
-   **`location=x`**: Exact match on location (e.g., `us-central1`, `us`).
-   **`column:x`**: Substring/token match on column names in the schema.
-   **`system=x`**: Exact match on source system. Common values: `bigquery`,
    `storage`, `biglake`, `cloud_sql`, `cloud_spanner`, `cloud_bigtable`,
    `pubsub`.
-   **`type=x`**: Exact match on entry type (e.g., `bigquery-table`,
    `storage-bucket`, `storage-folder`).
-   **`labels.key=value`**: (Semantic Mode ONLY) Exact match on a label.
-   **`label.key=value`**: (Keyword Mode ONLY) Exact match on a label.
-   **`createtime[>|<|=]x`**: Match assets created after/before date
    `YYYY-MM-DD`.
-   **`fully_qualified_name=x`**: Exact match on the FQN (e.g.,
    `bigquery:project.dataset.table`).

> [!TIP] Dataplex search results rely on metadata being ingested into the
> Universal Catalog (often via **Discovery Scans**). If an asset is missing from
> search, it may not be indexed. - **Fallback 1**: Try searching by the
> `fully_qualified_name` qualifier. - **Fallback 2**: Use native tools (e.g.,
> `bq show`, `gcloud storage`) or specific skills for that asset type if you
> already know the ID.

```bash
gcloud dataplex entries search "<KEYWORD_SEARCH_QUERY>" \
  --project="<PROJECT_ID>" \
  --limit=50
```

*Criteria*: Once candidate assets are returned, proceed to Step 3 using the
**full entry names** from the search results.

## Step 3: Lookup Entry

You MUST use the **Entries Lookup** command to fetch schema and deep metadata
for the relevant results obtained from Step 2.

> [!IMPORTANT] The argument MUST be the **name** (starting with `projects/`)
> returned by the search result. Passing short table IDs, GCS URIs, or fully
> qualified `bigquery:` prefixes is PROHIBITED and will fail.

### Command Execution

Use the `lookup_entry` MCP tool

OR

```bash
gcloud dataplex entries lookup "<FULL_ENTRY_NAME>"
```

*Completion Criteria*: The command returns the detailed schema and business
context.

--------------------------------------------------------------------------------

## Troubleshooting

### Lookup Fails or "Resource not found"

-   **Cause**: Short table names were used improperly.
-   **Fix**: Ensure you use the correct entry name format from the search
    results (starting with `projects/`).

### Search Returns No Results

-   **Cause**: Plural terms in keyword search or lack of scoping.
-   **Fix**: Switch to singular keywords. For semantic search, try more
    descriptive natural language.

### Lookup Fails with "NOT_FOUND" (despite correct format)

-   **Cause**: The table belongs to a project (e.g., `bigquery-public-data`)
    that has not fully synchronized its metadata with the Dataplex Universal
    Catalog. While the entry appears in search, `entries lookup` is unavailable.
-   **Fix**: Fall back to direct inspection using native tools (e.g., `bq` CLI).

### Search Fails with "--project: Must be specified."

-   **Cause**: `--project <PROJECT_ID>` arguments were not provided
-   **Fix**: Provide a project which will be used to authorize and attribute the
    search request.

### Search Fails with "PERMISSION_DENIED"

-   **Cause**: The project_id provided in the `--project <PROJECT_ID>` arguments
    does not have the Dataplex API enabled or the user is missing necessary IAM
    permissions.
-   **Fix**: Ask the user if they have a project which has the Dataplex API
    enabled with the dataplex.entries.get permission
