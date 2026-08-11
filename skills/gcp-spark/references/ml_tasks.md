# ML on Dataproc

**Verified patterns** for ML training:
- **XGBoost**: Use `SparkXGBClassifier`
- **Native Spark ML**: `GBTClassifier`, `RandomForestClassifier`,
  `LogisticRegression`

## Regression Modeling

> [!IMPORTANT]
> **Strict Guidelines for Regression Tasks in PySpark.** When working on regression tasks (e.g. predicting duration, prices), you MUST adhere to the following steps to avoid overfitting, data leakage, and improper evaluations:

1.  **Target Analysis**: Perform target analysis to understand the distribution of the target variable. Check if any transformation (e.g., log transformation) is needed.
2.  **Data Splitting**: Use an appropriate ratio, like 80/20 train/test split. Use `randomSplit([0.8, 0.2], seed=42)` for reproducibility.
3.  **Prevent Data Leakage (Avoid Premature Featurization)**: **NEVER** apply feature transformations (e.g. `StringIndexer`, `OneHotEncoder`, `StandardScaler`, `VectorAssembler`) to the entire dataset before splitting. You MUST assemble all feature transformations in a Spark ML `Pipeline` and fit the pipeline **ONLY** on the training set, then transform both train and test. This prevents information leaking from the test set into the training phase.
4.  **Train Multiple Models**: Train and compare multiple models (e.g., `LinearRegression`, `RandomForestRegressor`, `GBTRegressor`). 
5.  **Baseline Comparison**: Always establish a simple baseline for comparison before tuning complex models (e.g., a simple Mean Predictor, or `LinearRegression` without regularization).
6.  **Evaluate and Identify Overfitting**: Evaluate all models on **BOTH** the training set and the test set. Compare metrics (RMSE, R2, MAE) using `RegressionEvaluator` to identify if a model is overfitting (i.e. significantly better performance on train than test). 
7.  **Address Overfitting**: If a model overfits, address it by applying regularization (`regParam`, `elasticNetParam` in `LinearRegression`), reducing tree depth (`maxDepth` in trees), or increasing instances per node (`minInstancesPerNode`). 
8.  **Visualize Actual vs Predicted**: Provide a visualization of Actual vs. Predicted values, or a residual plot. Since data can be large, use `.sample(fraction, seed)` to downsample or extract it with `.toPandas()` *after* selecting predictions, ensuring you don't OOM the driver.

---

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
