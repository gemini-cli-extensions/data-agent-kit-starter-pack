# ML on Managed Spark

**Verified patterns** for ML training:

- **XGBoost**: Use `SparkXGBClassifier`
- **Native Spark ML**: `GBTClassifier`, `RandomForestClassifier`,
  `LogisticRegression`

## LightGBM on Managed Spark

> [!WARNING] **LightGBM has dependency conflicts on Managed Spark Serverless.**
> The SynapseML LightGBM wrapper conflicts with Managed Spark's internal
> libraries.

**Alternatives:**

1. **Use XGBoost** — Similar performance, native Spark support.
2. **Use Native Spark ML** — `GBTClassifier` provides similar gradient boosting
3. **Use Vertex AI** — Train LightGBM on Vertex, export model, load in Spark
   for inference
4.  **Use Managed Spark Cluster** (not Serverless) — More control over
    dependencies

**If you must use LightGBM**, consider:

-   Training on a dedicated Managed Spark cluster created with LightGBM spark
    packages set in the cluster properties:
    `spark:spark.jars.packages=com.microsoft.azure:synapseml_2.12:1.1.3`
-   **MUST** disable Managed Spark Autoscaling on the cluster
- Using ONNX model export for inference

---

## XGBoost Parameter Restrictions

> [!WARNING]
> **`SparkXGBClassifier` does NOT allow setting custom `objective` parameter.**
> The objective is automatically inferred from the classifier type:
> - `SparkXGBClassifier` → `binary:logistic` (inferred)
> - `SparkXGBRegressor` → `reg:squarederror` (inferred)

> [!WARNING]
> **`SparkXGBClassifier`** requires `dynamicAllocation=false`

**Prohibited** (causes `ValueError`):

```python
# ❌ DO NOT do this
xgb = SparkXGBClassifier(objective="binary:logistic", ...)
```

**Correct**:

```python
# ✅ Do this - objective is automatically set
xgb = SparkXGBClassifier(
    features_col="features",
    label_col="label",
    numRound=100,
    maxDepth=6,
)
```

See [XGBoost PySpark documentation]
(https://xgboost.readthedocs.io/en/stable/python/python_api.html#module-xgboost.spark)
for allowed parameters.
