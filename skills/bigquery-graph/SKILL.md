---
name: bigquery-graph
metadata:
  version: v1
description: >-
  Provides guidelines and best practices for querying and defining property graphs and semantic graphs in BigQuery using GQL (Graph Query Language). Use when creating property graphs or querying graph topologies in BigQuery.
---

# BigQuery Graph Analytics

BigQuery supports Graph Analytics through property graph queries (using GQL) and semantic graphs. Property graphs allow you to query topology, node/edge connections, and graph relationships directly in BigQuery SQL.

## Reference Directory

- **GQL Querying**: [graph_queries.md](references/graph_queries.md) - Standard GQL syntax and pattern matching.
- **Semantic Queries**: [semantic_queries.md](references/semantic_queries.md) - Semantic graph operations and expand functions.
- **Schema Best Practices**: [best_practices.md](references/graph-schema/best_practices.md) - Performance and indexing best practices for graph schemas.
- **DDL Reference**: [ddl_reference.md](references/graph-schema/ddl_reference.md) - `CREATE PROPERTY GRAPH` DDL syntax.
- **Feature Parity & Limitations**: [feature_parity.md](references/graph-schema/feature_parity.md) - GQL limitations and feature parity.
- **Graph Schema Advisor**: [graph_schema_ddl_advisor.md](references/graph-schema/graph_schema_ddl_advisor.md) - Assistant guidelines for designing graph schemas.

