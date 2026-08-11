# ML on Dataproc

**Verified patterns** for ML training:
- **XGBoost**: Use `SparkXGBClassifier`
- **Native Spark ML**: `GBTClassifier`, `RandomForestClassifier`,
  `LogisticRegression`

## LightGBM on Dataproc

> [!WARNING]
> **LightGBM has dependency conflicts on Dataproc Serverless.** The SynapseML
> LightGBM wrapper conflicts with Dataproc's internal libraries.

**Alternatives:**
1. **Use XGBoost** — Similar performance, native Spark support.
2. **Use Native Spark ML** — `GBTClassifier` provides similar gradient boosting
3. **Use Vertex AI** — Train LightGBM on Vertex, export model, load in Spark
   for inference
4. **Use Dataproc Cluster** (not Serverless) — More control over dependencies

**If you must use LightGBM**, consider:
- Training on a dedicated Dataproc cluster created with LightGBM spark packages
  set in the cluster properties:
  `spark:spark.jars.packages=com.microsoft.azure:synapseml_2.12:1.1.3`
- **MUST** disable Dataproc Autoscaling on the cluster
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

## Data Leakage Prevention

> [!CAUTION]
> **Data leakage** invalidates ML models. You MUST implement the following rules to avoid target, time, or group leakage.

1.  **Premature Featurization (Target/Feature Leakage)**: NEVER apply feature transformations (scaling, imputation, normalization, PCA, StringIndexer) *before* splitting the data. **ALWAYS** use a Spark ML `Pipeline` where feature engineering stages come *after* the train/test split.
2.  **Target Exclusion**: BEFORE creating a feature vector (`VectorAssembler`), explicitly exclude the target variable (label column) and any columns perfectly correlated or derived from the target (e.g., 'total_amount' if predicting 'tax_amount').
3.  **Group/Entity Leakage**: When predicting on grouped data (e.g., inventory items, customers, financial entities), DO NOT use random splits (`randomSplit`) across the entire dataset. You MUST group splits by entity ID or use a group-based splitting strategy to ensure an entity belongs entirely to training or testing, not both.
4.  **Hyperparameter Tuning Leakage**: NEVER use the holdout `test` set for hyperparameter tuning. ALWAYS use Cross-Validation (`CrossValidator`) or a separate `TrainValidationSplit` explicitly on the training data.
5.  **Time/Temporal Leakage**: For temporal data (e.g., financial transactions), NEVER use random splitting. You MUST split the data chronologically (train on past, test on future). Filter by a split date/timestamp to preserve chronological order.
