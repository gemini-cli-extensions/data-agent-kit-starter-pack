# Time Series & EDA in PySpark

> [!IMPORTANT]
> **ALWAYS** follow these strict guidelines when working on Time Series, EDA, or forecasting tasks in PySpark. If a dataset involves dates or timestamps, treat it as a Time Series task.

## 1. Datetime Handling & Feature Extraction
- **Datetime Conversion**: You MUST explicitly parse string columns representing time into proper timestamp/date types using `to_timestamp()` or `to_date()`.
- **Datetime Feature Extraction**: Extract relevant temporal features (e.g., year, month, day, dayofweek, hour, minute) into separate columns.
- **Handling Limited Data**: Recognize and explicitly discuss if the dataset has limited time span (e.g., only a few days or months of data) and how it impacts forecasting.

## 2. Exploratory Data Analysis (EDA) & Visualization
You MUST perform and explicitly discuss the following visualizations:
- **Target Visualization**: Plot the target variable over time (e.g., total sales vs. date). Describe trends and seasonality.
- **Distributions**: Visualize the distribution of continuous variables like price or amount (e.g., histograms or density plots for price distribution).
- **Temporal Patterns**: Investigate and visualize **daily patterns** (e.g., sales by day of week) and **hourly patterns** (e.g., volume by hour of day). Discuss these patterns.
- **Relationships**: Plot continuous variables against each other (e.g., price vs. amount) to find correlations.
- **Heatmaps**: Generate a correlation heatmap of numerical features.
- **Discussions & Investigations**: Always provide markdown cells in your notebook with a clear **pattern discussion** or **pattern investigation**. Explicitly state your findings.

## 3. Data Cleaning & Proper Feature Engineering
- **Outliers**: Explicitly treat and clean outliers in the context of Time Series (e.g., cap anomalies, remove unreasonable spikes, negative sales). Note that simple averages might be skewed.
- **Premature Featurization / Validation Leakage**: DO NOT apply scaling (like StandardScaler), imputation, or calculate global aggregates before splitting your data into train and test sets. Featurization MUST be fit only on the training set to prevent data leakage.
- **Information Usage**: Ensure you only use information that would actually be available at the time of prediction.

## 4. Stationarity Testing & Discussion
- **Stationarity Testing**: For Time Series forecasting, you MUST test for stationarity using a statistical test, such as the Augmented Dickey-Fuller (ADF) test.
  - *Note*: PySpark does not have a native ADF test. Convert the aggregated time series (which should be small enough) to a Pandas DataFrame and use `statsmodels.tsa.stattools.adfuller`.
- **Stationarity Discussion**: Explicitly discuss the ADF test results. If the data is non-stationary, explain why and apply necessary transformations (e.g., differencing, log transform) to achieve stationarity.

## 5. Splitting Strategy (Time & Group Leakage)
- **Time Leakage**: NEVER use random splitting (`randomSplit`) for time series modeling. You MUST split the data sequentially based on time (e.g., train on past, test on future) to prevent time leakage.
- **Group Leakage**: Be mindful of grouping variables (e.g., customers, store IDs). Make sure information from the test set does not bleed into the train set through overlapping groups, if the task requires generalizing to new groups.

## 6. Model Selection, Justification, and Implementation
- **Model Selection Logic / Justification**: Choose models that can effectively handle or be adapted for time series data (e.g., regression with lag features, tree-based models, specialized TS models). Provide a markdown cell justifying your model choice. 
- **Model Implementation**: Properly set up your PySpark ML pipelines (VectorAssembler, StringIndexer, etc.). Follow standard PySpark ML patterns.

## 7. Model Tuning & Evaluation
- **Hyperparameter Tuning**: You MUST perform hyperparameter tuning (e.g., using `CrossValidator` or `TrainValidationSplit` with a custom time-based fold if needed, or simple grid search).
- **Evaluation Metrics**: Evaluate the model using appropriate metrics for the problem (e.g., RMSE, MAE, R2 for regression). Always display these metrics clearly.

## 8. Forecasting & Visualizing Results
- **Visualizing Forecast vs Actual**: You MUST plot the predicted values against the actual values for the test/validation set on a timeline chart.
- **Retrain and Test**: If predicting completely unknown future values, after validating the model on a test set, you must retrain the chosen model on the *full* dataset (train + test) before making the final future forecast.

## 9. Summary, Conclusions, and Limitations
Provide a final, clear summary in markdown:
- **Summary & Conclusion**: Summarize the entire workflow, the final model performance, and the main findings.
- **Key Trends**: Reiterate the key trends discovered during EDA and modeling.
- **Limitations Discussion**: Explicitly discuss the limitations and caveats of your approach (e.g., assumptions made, missing variables, impact of limited data span).
