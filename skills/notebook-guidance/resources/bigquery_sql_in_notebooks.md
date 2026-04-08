# BigQuery in Notebooks

When working with BigQuery in a notebook (.ipynb) file, you MUST follow these
standards to ensure a seamless experience and proper data handling.

## BigFrames magics

Use BigFrames magics `%%bqsql` for BigQuery SQL queries. These cells support
native BigQuery SQL execution and data export to BigFrames dataframes with a
visually appealing interface.

> [!IMPORTANT]
>
> *   Unless specified by the user, **always use SQL for querying BigQuery.**
> *   DO NOT use the standard BigQuery Python client library
>     (`google.cloud.bigquery`) or `pandas.read_gbq`.
> *   **Mandatory dataframe export**: Always provide a dataframe name e.g.
>     `%%bqsql <df_name>`. This makes it easy to use results in follow up
>     Python cells.
> *   Verify that `bigframes` version number `2.38.0` and above is installed in
>     the notebook runtime environment. If it is missing,  ask the user if they
>     would like you to upgrade for them.

**Example %%bqsql magic usage:**

```python
# Initialize BigFrames and load %%bqsql magics
import bigframes
import bigframes.pandas as bpd
%load_ext bigframes
```

> [!CAUTION]
> Always use `%load_ext bigframes` exactly as shown. Do not load submodules —
> for example, `%load_ext bigframes.magics` or `%load_ext bigframes.bigquery`
> are not valid and must not be used.

> [!IMPORTANT]
> The `bigframes` library must be installed. Read the
> `managing-python-dependencies` skill to determine if it needs to be
> installed, and instructions for doing so.

```python
%%bqsql df_sample
SELECT * FROM `project.dataset.table` LIMIT 10
```

## Anti-patterns (NEVER DO THESE)

> [!CAUTION]
> 1.  **NO Python SDK for Queries**: Do not switch to
>     `client.query(sql).to_dataframe()` if SQL fails. Fix the SQL syntax
>     instead.
> 2.  **NO Mixing Logic**: Do not put Python code in the same cell as `%%bqsql`
>     magics.

## Working with SQL Results in Python

Magic cells with `%%bqsql <df_name>` produce a **BigQuery DataFrame**. In
subsequent cells, you can use `<df_name>` directly.

> [!IMPORTANT]
> You MUST use BigFrames for data exploration, manipulation, splitting etc.
> You MUST use BQML or bigframes.ml for machine learning tasks.
> You MUST NOT use pandas or Scikit-learn.

### BigQuery DataFrame Tips

*   **Avoid `.to_pandas()`**: You MUST NOT use `.to_pandas()` to download the entire dataset into memory. There are some exceptions:
    *  An error message explicitly requests you to use `to_pandas()`
    *  You are going to visualize the data, **and** the visualization library does not accept BigFrames Dataframe/Series instances. In this case, reduce the amount of data you are going to download before calling `.to_pandas()`
*   **Avoid `read_gbq()` for SQL**: Do not write SQL queries and execute them with `read_gbq()`. Use BigFrames Dataframe/Series methods instead.
*   **Use BigFrames ML package for Machine Learning Tasks**: Do not use Scikit-learn or other ML libraries with BigFrames dataframes. Import your tools/classes from `bigframes.ml`.
*   **Stay in the Cloud**: Perform data cleaning, transformation, and analysis via BigFrames methods to leverage BigQuery's scale.
*   **Accessors over UDFs/Lambdas**:
    *   Prefer built-in accessors (e.g., `df.col.str.*`, `df.col.dt.*`) over remote UDFs.
    *   **Do not use lambdas** with `Series.map()` or `DataFrame.apply()`.
*   **Schema Verification**: Do not assume schema of intermediate outputs. Check `.dtypes` after loading, and use `display()` with `.head()` or `.peek()`.
*   **Visualization**: BigFrames Dataframe mostly works directly with Matplotlib, Seaborn, and other ploting libraries. If your attempt didn't work, try using the "plot" accessor. If that didn't work either, you MUST sample or aggregate your data to make it small enough before calling "to_pandas()".
