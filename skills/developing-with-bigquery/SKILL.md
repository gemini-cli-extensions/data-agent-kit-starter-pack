---
name: developing-with-bigquery
description: |
  A repository of BigQuery-specific logic, knowledge, and specialized standards.
  Use this skill whenever you are doing anything with BigQuery, including:
    1. BigQuery query optimization
    2. BigFrames Python code
    3. BigQuery ML/AI functions.
license: TBD
metadata:
  version: v1
  publisher: google
---

This skill provides comprehensive guidance for BigQuery services, optimizations,
and data handling. It acts as a routing table for specialized BigQuery topics.

> [!IMPORTANT] For general standards on running BigQuery in notebooks (SQL
> cells, `export` keyword), see `@skill:notebook-guidance`.

> [!IMPORTANT] You MUST check the data size before deciding on which libraries
> to use. Use the data size to justify your decision.

Refer to the following resources for expert guidance on specific BigQuery
features:

### 1. Query Optimization

Performance and efficiency guidelines for BigQuery SQL. Includes rules for
column pruning, pushdown, and materialization strategies. - **Guide**:
[OPTIMIZATION.md](resources/OPTIMIZATION.md)

### 2. BigFrames (BigQuery DataFrames)

Guidelines for generating valid BigFrames code for data manipulation, model
development, and visualization. - **Guide**:
[BIGFRAMES.md](resources/BIGFRAMES.md)

Bigframes should be the default library/tool as it is more efficient than using
the BigQuery Python client library.

### 3. BigQuery ML & AI Functions (BQML SQL)

Usage rules and syntax standards for all BigQuery AI/ML functions via SQL
(Forecasting, Generative AI, Classification, etc.). - **Guide**:
[BQML.md](resources/BQML.md) - **Functions Reference**: -
[AI.FORECAST](resources/ai-forecast.md) -
[AI.EVALUATE](resources/ai-evaluate.md) -
[AI.GENERATE_TABLE](resources/ai-generate-table.md) -
[AI.GENERATE_EMBEDDING](resources/ai-generate-embedding.md) -
[Remote Models](resources/remote-models.md)
[CONTRIBUTION_ANALYSIS](resources/ml-contribution-analysis.md)
[VECTOR_SEARCH](resources/vector-search.md)

### 4. Notebook SQL cells

Refer to `@skill:notebook-guidance` for standards on running BigQuery in
notebooks.
