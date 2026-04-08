---
name: notebook-guidance
description: |-
  This skill guides the use of Jupyter notebooks for data analysis, exploration, and visualization, particularly with BigQuery. It outlines best practices for cell-by-cell execution and validation, library installation, and structuring notebooks for clarity. It also covers specific rules for data cleaning, plotting, and integrating with BigQuery SQL and machine learning workflows.
  Relevant when any of the following conditions are true:
    1. The user request involves a data analysis, data exploration, data visualization, or data insights task that requires multiple steps, queries, or visualizations to answer.
    2. The user explicitly requests a notebook (.ipynb).
    3. You are creating, editing, or executing cells in a Jupyter notebook.
    4. You need to query BigQuery from within a notebook. DO NOT use the Python BigQuery client library; instead, you MUST use the BigQuery SQL cells feature explained in this skill.
license: TBD
metadata:
  version: v1
  publisher: google
---

# Notebook Guidance

## When to Use a Notebook

Before choosing to use a notebook, evaluate the task complexity using these
heuristics.

Use a notebook if you meet at least one of these criteria: * 📈 **Data Insights &
Storytelling**: Use a notebook for any request to "give insights", "find
trends", "explore data", or "analyze data". These tasks benefit from using
visualizations to present the data. * 📊 **Visualizations are requested**: The
user explicitly asks for charts or plots. * 🔄 **Stateful / Iterative
Exploration**: You need to run a query, inspect results, and decide the next
query based on those results while keeping state in memory.

Do NOT use a notebook ONLY if: * 📝 **Simple Fact/Status**: The request only
requires a single number (e.g., "how many rows") or a status check (e.g., "when
was this table updated"). * 🏃‍♂️ **Schema Preview**: The request is only about
the schema or field types.

**Golden Rule of Data Storytelling:** If any analytical insight, trend, or
comparison is involved, favor a notebook and a visualization. A notebook is the
"standard" environment for our developer workflow; do not avoid it because of
"overhead".

## Notebook Best Practices

The golden rule: **STEP BY STEP GENERATE CELL -> EXECUTE CELL -> VALIDATE
OUTPUT**, do not generate the entire notebook all at once.

1.  **EXECUTE-AND-VALIDATE LOOP**: Generate ONE cell, execute it, then verify
    the output. If the output is data (e.g. a dataframe), you MUST inspect it to
    confirm the logic is correct before generating the next step. Batch
    generation of an entire notebook is strictly prohibited because error
    propagation in notebooks is expensive to fix.
2.  **IDENTIFY DATA EARLY**: Use `@skill:discovering-gcp-data-assets` or
    BigQuery list tools to find the correct `project.dataset.table` before
    writing ANY code. If the table ID is missing, ask the user.
3.  **CLEAN FINAL STATE**: The final notebook MUST NOT have failed cells. If a
    cell fails, you MUST fix it. If you tried several versions, delete the
    failed attempts before you present the notebook to the user.
4.  **LOGICAL CHUNK FIDELITY**: Keep cells small. One logical transformation or
    visualization per cell. Group related cells into logical units (e.g., a
    BigQuery SQL query cell followed immediately by a Python visualization cell
    for those results). Use descriptive **markdown cells** to separate and
    document different logical sections.
5.  **GENERATE VISUALIZATIONS**: Always accompany data insights with
    visualizations; charts are often more effective than raw numbers for
    communicating trends and comparisons.

## Kernel & Environment Management

Notebooks run in specific **Kernels** (execution backends). You MUST ensure the
kernel’s Python environment contains the necessary libraries (`bigframes`,
`ipykernel`, etc.).

### Kernel Types

1.  **Local Python**: Standard Python 3 kernel running on the notebook host
    (Managed instance, local machine).
2.  **Cloud Spark Remote (Dataproc Serverless)**: Transient Spark environment
    managed by GCP. Use for large-scale data processing.
3.  **Cloud Spark Remote (Dataproc Cluster)**: Persistent Spark clusters for
    shared or custom configurations.
4.  **Colab (Managed)**: Ephemeral Google-managed runtimes.

### No Active Kernel / Setup Check

1.  **Infer or Ask about Kernel Preferences**:
    -   **Infer from Context**:
        -   If the task mentions "Spark", "PySpark", or "distributed compute",
            or if the active workspace is already a Spark cluster, lean towards
            **Remote Spark**.
        -   If the task is focused on "BigQuery", "BigFrames", or standard API
            calls, lean towards **Local Python**.
    -   **Ask when Ambiguous**: If multiple options fit, ask if they prefer a
        **Local Python** or a **Cloud/Remote Kernel** (e.g., Colab, Spark).
2.  **For Local Setup**: Use `@skill:managing-python-dependencies` to verify
    if a virtual environment exists. If not, create one. Ensure `ipykernel` is
    installed in that environment. Install any other relevant libraries.
3.  **For Remote Setup**: Advise the user to use the UI to select the
    appropriate remote kernel.

### Proper Library Installation

#### 1. Local Kernels

Before installing any python libraries, you MUST use
`@skill:managing-python-dependencies` to detect how python dependencies are
managed in the project.

#### 2. Remote Kernels (Spark/Colab)

Since these are often ephemeral or managed by GCP:

*   Use `%pip install <package>` in the first cell if it's the only way to
    modify the runtime.
*   Check if the library is already available in the pre-installed stack.

When in doubt about the kernel type or preferred installation method, ask the
user for clarification.

## Data Analysis & Visualization Rules

Guidelines for performing exploratory data analysis, data cleaning, and
visualization in notebooks.

### Notebook Layout

The notebook should read like a story. While you have flexibility (e.g.,
multiple visualizations for one data cell, or data cells building on each
other), aim for this general flow:

1.  **Title & Objective** (Markdown Cell)
    *   What is this notebook for? (e.g., `# Retention Analysis`)
2.  **Section Header** (Markdown Cell)
    *   What are we looking at now? (e.g., `## Exploring User Retention`)
3.  **Data Acquisition/Transformation** (SQL or Python Cell)
    *   Query BigQuery or transform data.
4.  **Verification (Optional but Recommended)** (Python Cell)
    *   `df.head()` or assert sanity checks.
5.  **Visualization (The Goal)** (Python Cell)
    *   Plot the insight (e.g., `df.plot()`).

*Repeat steps 2-5 for each new sub-topic or insight. You can have multiple Data
cells before a Visualization, or multiple Visualizations from one Data cell. The
key is to keep them grouped logically and separated by Markdown headers.*

1.  **Final Summary** (Markdown Cell)

    *   At the end of the notebook, add a markdown cell containing a summary
        paragraph that summarizes the findings to the user. The summary MUST
        follow these guidelines:
    *   MUST NOT add Python code to the summary.
    *   The summary MUST NOT start with a code block.
    *   The summary MUST be strictly grounded in the numerical data verified in
        the notebook.
    *   The summary MUST ONLY contain the following three sections:
        *   ### Q&A If the data analysis task contains questions (implied or
            explicit), you MUST answer them based on the solving process. Skip
            this section if there are no questions to answer.
        *   ### Data Analysis Key Findings Summarize the key analysis findings
            in bullet points, it's a plus to quote the numbers in the previous
            steps. Only report high-value findings, skip the obvious ones.
        *   ### Insights or Next Steps Provide 1-2 concise insights or next
            steps in bullet points.

2.  **Next Steps**: After you are done generating and executing the entire
    notebook successfully, and the summary is complete, notify the user and
    propose next step suggestions.

### Plotting Rules

1.  You MUST use different colors for different features to ensure plots are
    readable for humans.
2.  When creating a plot, you MUST adjust the figure size based on the number of
    features. The labels and legends MUST NOT overlap.
3.  You SHOULD arrange the layout wisely. Using subplots CAN help in placing
    different plots effectively.
4.  You MUST use inline figures to present figures and plots along with code and
    text in the notebook.
5.  For clustering, use PCA to reduce to 2D before scatter plotting.
6.  Use **Line Charts** ONLY for continuous data (e.g. time series) where
    interpolation between points is meaningful.

### Data Cleaning Rules

1.  You MUST be careful about missing values and duplicated values.
2.  You MUST NOT drop columns unless absolutely necessary. Dropping columns is
    irreversible.
3.  You SHOULD focus on columns directly related to accomplishing the task; not
    every column NEEDS to be cleaned.

## Specialized Notebook Guidance

Refer to the following resources for guidance on specific notebook topics:

### 1. BigQuery in Notebooks

Standards for using BigQuery SQL in notebooks and accessing results in Python.

-   **Guide**:
    [bigquery_sql_in_notebooks.md](resources/bigquery_sql_in_notebooks.md)
    and the BigQuery skills.
-   **MUST READ WHEN**: You are writing BigQuery SQL queries in a notebook or
    processing query results in Python.

### 2. Machine Learning in Notebooks

Integration with machine learning workflows and best practices. - **Guide**: Use
`@skill:ml-best-practices`. - **MUST READ WHEN**: The task involves machine
learning, training a model, clustering, classification, regression, or
time-series forecasting.

If any "MUST READ WHEN" condition is met, you MUST read the corresponding guide
before proceeding.
