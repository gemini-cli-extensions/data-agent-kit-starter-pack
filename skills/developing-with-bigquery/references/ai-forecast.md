# AI.FORECAST
Used for time-series forecasting without model training. It automatically
detects frequency (daily, weekly, etc.) based on your timestamp column.

## Syntax
```sql
SELECT
  *
FROM
  AI.FORECAST(
    { TABLE `project.dataset.table` | (QUERY_STATEMENT) },
    data_col => 'DATA_COL',
    timestamp_col => 'TIMESTAMP_COL'
    [, model => 'MODEL']
    [, id_cols => ID_COLS]
    [, horizon => HORIZON]
    [, confidence_level => CONFIDENCE_LEVEL]
    [, output_historical_time_series => OUTPUT_HISTORICAL_TIME_SERIES]
    [, context_window => CONTEXT_WINDOW]
  )
```

## Input Arguments
| Argument | Requirement | Type | Description |
| :--- | :--- | :--- | :--- |
| **`input_data`** | **Required** | | The source table or subquery containing historical data. |
| **`data_col`** | **Required** | String | The numeric column to predict. |
| **`timestamp_col`** | **Required** | String | The column containing dates/timestamps. |
| **`id_cols`** | Optional | Array<String> | Grouping columns for multiple series (e.g., `['store_id']`). |
| **`horizon`** | Optional | Int64 | Number of future points to predict. Defaults to 30. |
| **`confidence_level`** | Optional | Float64 | Confidence interval (0 to 1). Defaults to 0.95. |
| **`model`** | Optional | String | Model version. Defaults to `'TimesFM 2.0'`. |
| **`context_window`** | Optional | Int64 | The number of historical data points the model uses to forecast. Max 512. If not set, the model determines this automatically. |

## Output Schema
The schema adjusts based on the `output_historical_time_series` flag.

| Column | Type | Included if output_historical_time_series=FALSE | Included if output_historical_time_series=TRUE | Description |
| :--- | :--- | :---: | :---: | :--- |
| **`id_cols`** | (As Input) | Yes | Yes | Original identifiers for the series. |
| **`forecast_timestamp`** | TIMESTAMP | **Yes** | No | Timestamp for predicted points. |
| **`forecast_value`** | FLOAT64 | **Yes** | No | The 50% quantile (median) prediction. |
| **`time_series_timestamp`** | TIMESTAMP | No | **Yes** | Uniform timestamp column for both history and forecast. |
| **`time_series_data`** | FLOAT64 | No | **Yes** | Merged column: actual values for history, median for forecast. |
| **`time_series_type`** | STRING | No | **Yes** | Label: `'history'` or `'forecast'`. |
| **`prediction_interval_lower_bound`** | FLOAT64 | Yes | Yes | Lower bound (NULL for historical rows). |
| **`prediction_interval_upper_bound`** | FLOAT64 | Yes | Yes | Upper bound (NULL for historical rows). |
| **`confidence_level`** | FLOAT64 | Yes | Yes | The constant confidence level used. |
| **`ai_forecast_status`** | STRING | Yes | Yes | Error messages or empty string on success. |

## Example: Forecasting with History

```sql
-- Forecast next 10 days of sales by store and include historical data for charting
SELECT * FROM AI.FORECAST(
  TABLE `my_project.sales.daily_totals`,
  data_col => 'total_sales',
  timestamp_col => 'date',
  id_cols => ['store_id'],
  output_historical_time_series => TRUE
);
```