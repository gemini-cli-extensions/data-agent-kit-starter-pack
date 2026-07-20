---
name: bigquery
description: |
  Provides BigQuery-specific logic, knowledge, and specialized standards.
  Use this skill whenever you are doing anything with BigQuery, including:
    1. BigQuery query optimization (SQL)
    2. BigFrames Python code
    3. BigQuery ML/AI functions (SQL & Python)
    4. Graph Analytics (GQL & Property Graphs)
license: Apache-2.0
metadata:
  version: v4
  publisher: google

---

This skill provides comprehensive guidance for BigQuery services, optimizations,
and data handling. It acts as a routing table for specialized BigQuery topics.


> [!IMPORTANT]
>
> You MUST check the data size before deciding on which libraries to use. Use
> the data size to justify your decision.

Refer to the following resources for expert guidance on specific BigQuery
features:

### 1. Query Optimization

Performance and efficiency guidelines for BigQuery SQL. Includes rules for
column pruning, pushdown, and materialization strategies.

- **Guide**: [OPTIMIZATION.md](references/sql/OPTIMIZATION.md)

### 2. BigFrames (BigQuery DataFrames)

Guidelines for generating valid BigFrames code for data manipulation, model
development, and visualization.

- **Guide**: [BIGFRAMES.md](references/bigframes/BIGFRAMES.md)

Bigframes should be the default library/tool as it is more efficient than using
the BigQuery Python client library.

### 3. BigQuery ML & AI Functions (BQML SQL)

Usage rules and syntax standards for all BigQuery AI/ML functions via SQL
(Forecasting, Generative AI, Classification, etc.).

- **Best Practices**: [ai_function_best_practices.md](references/ai-ml/ai_function_best_practices.md)
- **Functions Reference**:

  - **AI.CLASSIFY**: [ai_classify.md](references/ai-ml/ai_classify.md) - Classify text.
  - **AI.DETECT_ANOMALIES**: [ai_detect_anomalies.md](references/ai-ml/ai_detect_anomalies.md) - Detect anomalies.
  - **AI.EVALUATE**: [ai_evaluate.md](references/ai-ml/ai_evaluate.md) - Evaluate models.
  - **AI.FORECAST**: [ai_forecast.md](references/ai-ml/ai_forecast.md) - Time-series forecasting.
  - **AI.GENERATE**: [ai_generate.md](references/ai-ml/ai_generate.md) - Generate text using LLMs.
  - **AI.GENERATE_EMBEDDING**: [ai_generate_embedding.md](references/ai-ml/ai_generate_embedding.md) - Generate embeddings.
  - **AI.GENERATE_TABLE**: [ai_generate_table.md](references/ai-ml/ai_generate_table.md) - Table-valued AI generation.
  - **AI.IF**: [ai_if.md](references/ai-ml/ai_if.md) - Evaluate semantic conditions.
  - **AI.KEY_DRIVERS**: [ai_key_drivers.md](references/ai-ml/ai_key_drivers.md) - Identify key drivers.
  - **AI.SCORE**: [ai_score.md](references/ai-ml/ai_score.md) - Score data.
  - **AI.SEARCH**: [ai_search.md](references/ai-ml/ai_search.md) - Semantic search.
  - **AI.SIMILARITY**: [ai_similarity.md](references/ai-ml/ai_similarity.md) - Semantic similarity.
  - **Remote Models**: [remote_models.md](references/ai-ml/remote_models.md) - Working with remote models (Vertex AI).
  - **CONTRIBUTION_ANALYSIS**: [ml_contribution_analysis.md](references/ai-ml/ml_contribution_analysis.md) - Step-by-step contribution analysis.
  - **VECTOR_SEARCH**: [vector_search.md](references/ai-ml/vector_search.md) - Vector search best practices.

### 4. Graph Analytics (Property Graphs & GQL)

Guidelines and best practices for querying property graphs in BigQuery.

- **Property Graph Guidelines**: [graph_queries.md](references/graph/graph_queries.md) - Standard GQL syntax and query patterns.
- **Semantic Graph Guidelines**: [semantic_queries.md](references/graph/semantic_queries.md) - Semantic graph operations and expand functions.
-   **Graph Schema DDL Advisor**:
    [graph_schema_ddl_advisor.md](references/graph/graph-schema/graph_schema_ddl_advisor.md)
    -   Assists in defining, correcting, and optimizing BigQuery Property Graph
        and Semantic Graph schemas.
