# Feature Engineering

> [!IMPORTANT] Always follow these patterns when requested to perform Feature
> Engineering tasks.

## One-Hot Encoding

When asked to one-hot encode categorical features (like a flag or status), you
MUST use `pyspark.ml.feature.StringIndexer` paired with
`pyspark.ml.feature.OneHotEncoder`. Do not manually translate columns unless
explicitly asked.

```python
from pyspark.ml.feature import StringIndexer, OneHotEncoder

# Index the categorical column
indexer = StringIndexer(inputCol="preferred_customer_flag", outputCol="preferred_customer_index")
df = indexer.fit(df).transform(df)

# One-hot encode the index
encoder = OneHotEncoder(inputCols=["preferred_customer_index"], outputCols=["preferred_customer_vec"])
df = encoder.fit(df).transform(df)
```

## Creating Target Labels (e.g., Churn)

When creating binary target labels (like labeling zero purchases in the last 30
days as churn), use `pyspark.sql.functions.when`:

```python
from pyspark.sql.functions import col, when

df = df.withColumn(
    "churn",
    when(col("purchases_last_30_days") == 0, 1).otherwise(0)
)
```

## Train/Test Data Splitting

When you need to split data for train and test:

```python
train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
```

## Outputting Split Datasets to GCS

When asked to output train and test datasets to subdirectories:

```python
# Output train data
train_df.write.mode("overwrite").parquet("gs://bucket-name/path/to/feature_engineering/train/")

# Output test data
test_df.write.mode("overwrite").parquet("gs://bucket-name/path/to/feature_engineering/test/")
```
