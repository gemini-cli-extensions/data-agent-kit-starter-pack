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

## Clustering & Statistical Testing Validity

When performing Clustering and Statistical Data Analysis tasks, you MUST adhere
to the following best practices to ensure high-quality and valid evaluations:

### Clustering Process

-   **Initial Visualization**: You MUST perform initial exploratory
    visualization before formulating clusters (e.g., univariate distributions,
    pairplots, or PCA scatterplots) to understand the data.
-   **Parameter Optimization**: Determine the optimal number of clusters (`K`)
    dynamically using data-driven methods, such as computing and plotting the
    Silhouette Score (`pyspark.ml.evaluation.ClusteringEvaluator`) or the Elbow
    method via WSSE across a range of `K` values.
-   **Evaluation**: Report numerical evaluation metrics of the model (e.g.,
    using `ClusteringEvaluator`).
-   **Cluster Visualization**: Generate 2D scatter plots demonstrating cluster
    separation (often by applying PCA to the feature vectors to reduce down to 2
    dimensions).
    -   Each cluster MUST be represented by a **distinct color**.
    -   All scatterplots MUST include a distinct **legend** identifying each
        cluster label.
-   **Cluster Understanding & Description**:
    -   Create a summary DataFrame grouping by the cluster label and calculating
        means/medians of the original features
        (`df.groupBy('prediction').mean().show()`). Describe the distinctive
        profile of each cluster.
    -   Visualize the **Cluster Size Distribution** (e.g., plot the count of
        records assigned to each cluster as a bar chart).
    -   Explicitly compute and discuss **Cluster separation** and **purity**
        relative to distinct business characteristics (like loan status or
        customer types, if relevant).

### Statistical Testing and Exploratory Analysis (e.g. Finance & Loan Data)

-   **Univariate Visualization & Analysis**: Perform robust distribution
    analysis containing histograms, density plots, or box plots. Provide clear
    descriptive insights for these distributions.
-   **Handling Distributions**: Address skewed target distributions properly
    (e.g., log-transformers, normalizers, clipping) before using them
    mathematically.
-   **Multivariate Correlation & Visualization**: You MUST produce multivariate
    visualizations (like correlation matrices or heatmaps).
    -   Ensure logical business validities are verified (e.g., check that
        `amount` positively correlates with `payments`, and define relationships
        correctly between `duration` vs `amount`).
-   **Temporal Analysis**: When timestamp/date features are available, you MUST
    visualize and investigate the temporal trends and evolution of key variables
    across time.

*NOTE: While PySpark processes DataFrames, producing these visualizations
efficiently often requires bringing a sample or the aggregated results into a
pandas DataFrame (e.g., `df.sample(fraction=0.1).toPandas()`) or plotting
aggregated forms directly.*
