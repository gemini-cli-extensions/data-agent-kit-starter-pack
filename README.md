# Data Agent Kit Starter Pack

> [!NOTE]
> This extension is currently in beta (pre-v1.0), and may see breaking changes until the first stable release (v1.0).

This plugin provides a specialized suite of skills and MCP tools for data engineers and database practitioners working on Google Cloud. It acts as an expert assistant, allowing you to use natural language prompts in your preferred coding agent to architect complex data pipelines, transform data with dbt, write Spark and BigQuery SQL notebooks, and orchestrate end-to-end workflows across the Google Cloud data ecosystem (BigQuery, Spanner, BigLake, Dataproc, etc.).

> [!IMPORTANT]
> **We Want Your Feedback!**
> Please share your thoughts with us by opening an issue on GitHub. Your input is invaluable and helps us improve the project for everyone.

## Why Use the Data Agent Kit Starter Pack?

* **Seamless Workflow:** Bring Google Cloud data engineering expertise directly into your terminal or IDE via Gemini CLI, Claude Code, or Codex.
* **End-to-End Data Pipelines:** Effortlessly generate code that reads raw data from Cloud Storage, processes it with Spark or BigQuery, transform it through medallion architectures (bronze, silver, gold) using dbt, and export it to serving layers like Spanner.
* **Ecosystem Integration:** Work across boundaries—generate BigLake Iceberg catalog tables, train BigQuery ML models (XGBoost, KMEANS), and create interactive Streamlit dashboards or LookML models, all from natural language.
* **Workflow Orchestration:** Automatically create and schedule orchestration pipelines that tie your notebooks and dbt models together into robust, scheduled jobs.

## Prerequisites

Ensure you have the following installed:
* **Node.js and npm** (Latest version recommended)
* One of the following coding agents:
    * [Gemini CLI](https://github.com/google-gemini/gemini-cli) (v0.6.0+)
    * [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
    * Codex CLI
* **(Optional) IDE Extension:** [Google Cloud Data Agent Kit](https://docs.cloud.google.com/data-cloud-extension/vs-code/install).

## Getting Started

### Installation

Choose the installation method for your preferred coding agent. Run the commands in terminal

<details>
<summary><b>Gemini CLI and Gemini Code Assist</b></summary>

```bash
gemini extensions install https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack
```
</details>

<details>
<summary><b>Claude Code</b></summary>

Run the `claude` command to start the agent, then run:

```bash
/plugin marketplace add https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack
/plugin install data-agent-kit-starter-pack@data-agent-kit-starter-pack-marketplace
```
</details>

<details>
<summary><b>Codex</b></summary>

Run the following commands in your terminal:

**macOS / Linux:**
```bash
curl -sSL https://raw.githubusercontent.com/gemini-cli-extensions/data-agent-kit-starter-pack/main/codex-install.sh | bash
```

**Windows:**
```powershell
irm https://raw.githubusercontent.com/gemini-cli-extensions/data-agent-kit-starter-pack/main/codex-install.ps1 | iex
```

After running the installation script, run the `codex` command to start the agent, then run:

```bash
/plugins
```

Use the interactive options to install the extension with the name `Data Agent Kit Starter Pack`.
</details>

### Configuration

MCP toolboxes are added to the respective agent configuration files. You must configure the MCP toolboxes in your agent's configuration files for them to start successfully.

In all cases, you must restart the agent after updating the configuration files.

<details>
<summary><b>Gemini CLI and Gemini Code Assist</b></summary>

Edit the configuration file:
`~/.gemini/extensions/data-agent-kit-starter-pack/gemini-extension.json`
</details>

<details>
<summary><b>Claude Code</b></summary>

1. Edit the configuration file:
`~/.claude/plugins/cache/data-agent-kit-starter-pack-marketplace/data-agent-kit-starter-pack/<version>/.mcp.json`

2. Reinstall the plugin:
Run `/plugin` and use interactive options to uninstall `data-agent-kit-starter-pack`. Then run `/plugin install` to add it back.
</details>

<details>
<summary><b>Codex</b></summary>

1. Edit the configuration file:
`~/.agents/plugins/data-agent-kit-starter-pack/.mcp.json`

2. Use interactive options to uninstall and install the extension:
```bash
/plugins
```
Install with name: `Data Agent Kit Starter Pack`
</details>

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

Your agent has the power to execute tools and commands on your behalf. Protect your GCP resources by enforcing **Strict Least Privilege** across all CLIs, MCP servers and other resources available to your agents.

*   Use [service accounts](https://docs.cloud.google.com/docs/authentication/use-service-account-impersonation) for accessing your cloud resources.
*   Assign the service account a role with [limited permissions](https://docs.cloud.google.com/iam/docs/roles-overview).
*   Prevent unwanted cross-org agent access by utilizing **Principal Access Boundaries** to scope your agent to [projects](https://docs.cloud.google.com/iam/docs/principal-access-boundary-policies#use-case-one-project) you intend the agent to access.

> [!NOTE]
> The Principal Access Boundary condition should bind the policy to the service accounts you intend to restrict.
