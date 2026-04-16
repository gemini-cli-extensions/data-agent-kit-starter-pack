# Data Cloud AI Dev Kit

> [!NOTE]
> This extension is currently in beta (pre-v1.0), and may see breaking changes until the first stable release (v1.0).

This plugin provides a specialized suite of skills and MCP tools for data engineers and database practitioners working on Google Cloud. It acts as an expert assistant, allowing you to use natural language prompts in your preferred coding agent to architect complex data pipelines, transform data with dbt, write Spark and BigQuery SQL notebooks, and orchestrate end-to-end workflows across GCP's data ecosystem (BigQuery, Spanner, BigLake, Dataproc, etc.).

> [!IMPORTANT]
> **We Want Your Feedback!**
> Please share your thoughts with us by opening an issue on GitHub. Your input is invaluable and helps us improve the project for everyone.

## Why Use the Data Cloud AI Dev Kit?

* **Seamless Workflow:** Brings Google Cloud data engineering expertise directly into your terminal or IDE via Gemini CLI, Claude Code, or Codex.
* **End-to-End Data Pipelines:** Effortlessly generate code that reads raw data from GCS, processes it with Spark or BigQuery, transforms it through medallion architectures (bronze, silver, gold) using dbt, and exports it to serving layers like Cloud Spanner.
* **Ecosystem Integration:** Work across boundaries—generate BigLake Iceberg catalog tables, train BigQuery ML models (XGBoost, KMEANS), and create interactive Streamlit dashboards or LookML models all from natural language.
* **Workflow Orchestration:** Automatically create and schedule orchestration pipelines that tie your notebooks and dbt models together into robust, scheduled jobs.

## Prerequisites

Ensure you have the following installed:
* **Node.js and npm** (Latest version recommended)
* One of the following coding agents:
    * [Gemini CLI](https://github.com/google-gemini/gemini-cli) (v0.6.0+)
    * [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
    * Codex CLI

## Getting Started

### Installation

Choose the installation method for your preferred coding agent.

#### Gemini CLI
```bash
gemini extensions install https://github.com/gemini-cli-extensions/data-cloud-ai-dev-kit
```

#### Claude Code
```bash
/plugin marketplace add https://github.com/gemini-cli-extensions/data-cloud-ai-dev-kit
/plugin install data-cloud-ai-dev-kit@data-cloud-ai-dev-kit-marketplace
```

#### Codex
**macOS / Linux:**
```bash
gh api repos/gemini-cli-extensions/data-cloud-ai-dev-kit/contents/codex-install.sh -H "Accept: application/vnd.github.raw" | bash
```

**Windows:**
```powershell
gh api repos/gemini-cli-extensions/data-cloud-extension/contents/codex-install.ps1 -H "Accept: application/vnd.github.raw" | powershell -ExecutionPolicy Bypass -
```

## Usage Examples

Interact with your coding agent using natural language prompts to perform complex data engineering tasks:

* **Data Ingestion & Processing:**
  * "Create a Spark notebook that reads raw fraud transaction data from gs://fin-clearing-west1/raw, deduplicates records, and writes hourly partitions to a BigLake Iceberg catalog table."
  * "Create a BigQuery SQL notebook that drops an existing table and writes deduplicated transaction data from GCS."
* **Data Transformation (dbt):**
  * "Create a dbt pipeline to transform bronze_transactions into silver and gold tables, standardizing timestamps and joining with identity tables."
* **Machine Learning & Serving:**
  * "Train a robust XGBoost model using BigQuery ML on the gold_transactions table to identify potential fraud."
  * "Generate an inference notebook to batch-process new partitions and write flagged transactions into a Cloud Spanner table for high-availability access."
* **Analysis & Visualization:**
  * "Generate a complete View for my BigQuery tables to show YoY revenue growth, then generate a LookML model and an interactive Streamlit dashboard prototype."
* **Orchestration:**
  * "Create an orchestration pipeline that first runs the dedup notebook, then the dbt pipeline, and finally the model training and inference notebooks. Schedule it to run every Monday morning."


## Troubleshooting

* **Plugin Not Found:** Ensure you have restarted your agent (e.g., Gemini CLI or Codex) after installation.
* **Authentication Errors:** Many GCP skills require an active authenticated session. Ensure you have run `gcloud auth login` and `gcloud auth application-default login` on your machine.
* **MCP Connection Issues:** Update the MCP server configurations such as project, region etc. needed by MCP toolboxes in order to connect successfully to them.

## Security Reminder: Agent Environment Hardening

Your agent has the power to
execute tools and commands on your behalf. Protect your GCP resources by
enforcing **Strict Least Privilege** across all CLIs, MCP servers and other
resources available to your agents. For example, use scoped Service Accounts
(read more
[here](https://docs.cloud.google.com/docs/authentication/use-service-account-impersonation))
for tasks accessing your cloud resources and conducting regular permission and
agent settings audits to minimize your attack surface.
