# BigQuery Optimization

Performance and efficiency guidelines for BigQuery SQL queries.

## SQL Optimization Rules

> [!TIP]
> Always include a **"Summary of Optimizations"** section listing only the optimizations applied.

### Always Apply (Automatic)

| Optimization | Description |
| --- | --- |
| **Column Pruning** | Remove unnecessary columns from all query stages. |
| **Common Subexpression Reuse** | Factor out identical expressions to avoid redundant computation. |
| **Predicate Pushdown** | Apply `WHERE` filters as early as possible. |
| **Early Aggregation** | Perform `GROUP BY` before joins when possible. |
| **Intermediate Materialization** | Choose `VIEW` vs `TABLE` for intermediate nodes based on efficiency. |

#### Intermediate Node Strategy

| Strategy | When to Use |
| --- | --- |
| **`VIEW`** | Small datasets or simple transformations. |
| **`TABLE`** | Large datasets, expensive computations, or nodes reused multiple times. |

### Always Rewrite (Mandatory)

| Pattern | Replace With |
| --- | --- |
| `WHERE <col> IN (SELECT ...)` | `WHERE EXISTS (SELECT 1 FROM ...)` |
| `WHERE (SELECT COUNT(*) ...) > 0` | `WHERE EXISTS (SELECT 1 FROM ...)` |

### Propose with Confirmation (Conditional)

- **`UNION` → `UNION ALL`**: Faster (skips deduplication), but permits duplicate rows.
- **`COUNT(DISTINCT)` → `APPROX_COUNT_DISTINCT`**: Faster and lower memory, but approximate.
