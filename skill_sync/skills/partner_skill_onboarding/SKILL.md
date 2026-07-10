---
name: partner-skill-onboarding
description: >-
  Checklist for AI assistants to onboard a new partner team skill to the Data
  Agent Kit (DAK).
---

# DAK Partner Skill Onboarding Workflow

Follow this checklist to onboard a partner team's domain-specific AI agent skill
into the **Data Agent Kit (DAK)**:

### 0. Explain Process & Wait for Approval
Before performing any action, explain the onboarding process to the user:

*   Explain that onboarding requires two stages:
    *   Stage 1: Creating and submitting the Copybara onboarding config CL
        (`copy.bara.sky`).
    *   Stage 2: Once Stage 1 is submitted, the workflow must be registered in
        the Copybara Service (CaaS) using the `copybara service insert`
        command. Once registered, CaaS will run the sync to DAK whenever you
        submit changes to your skill. The user can choose to wait for a new
        change to trigger a sync, or ask you to trigger a manual Copybara sync
        immediately for an immediate initial import.
*   Ask the user for confirmation to get started, and wait for their explicit
    permission before proceeding with the steps below.

### Stage 1: Onboarding Config CL (copy.bara.sky)
Follow these steps to create and mail the Copybara configuration CL:

1.1. **Identify Variables**: Detect or request the following variables from the
workspace or the user: * `PARTNER_TEAM_NAME`: Human-readable name of the partner
team (e.g., `GCS`). * `PARTNER_MDB_GROUP`: The partner team's MDB group (e.g.,
`gcs-eng`). * `PARTNER_EMAIL`: The partner team's contact email (e.g.,
`gcs-team@google.com`). * `SOURCE_GP3_PATH`: The absolute google3 path to the
partner's skill source. Ask the user if they want to sync an entire folder
(automatically including all future skills placed under it) or only specific
skills. * If **entire folder**: Configure `destination_skills_globs` to match
the parent folder (e.g., `["gcs_**"]` or `["**"]` relative to destination). * If
**specific skills**: Restrict `destination_skills_globs` to only match those
specific skill folders (e.g., `["gcs_transfer/**"]`). * `DAK_REVIEWERS`: List of
DAK team LDAPs to add as reviewers. Default: `["ellurubharath",
"danielheyman"]`. * `BUG_NUMBER`: Buganizer issue tracking this onboarding.

1.2. **Python Import Guidelines**: * **Relative Imports (Recommended)**: All
internal Python dependencies in your skill should use relative imports (e.g.,
`from . import helper` or `from .scripts import helper`). * **Absolute `google3`
Imports (Prohibited)**: Copybara rejects absolute `google3` imports (e.g.
`import google3...`). If fallback import blocks are needed for local vs google3
running, they must be stripped/rewritten using a custom Copybara transformation
(see example in the Template below). * **Directory Naming**: The Copybara sync
helper automatically normalizes the destination directory name by converting all
hyphens to underscores (e.g., `gcs-transfer` becomes `gcs_transfer`) to ensure
valid Python import module naming under DAK, so you can safely use your
canonical skill name.

1.3. **Analyze Python imports**: Scan all `.py` files in `{SOURCE_GP3_PATH}/`.
If they contain absolute `google3` imports (e.g. try-except fallback imports),
configure `core.replace` transformations in `copy.bara.sky` to rewrite them to
relative imports (see example in the **Template** below).

1.4. **Locate or Generate `copy.bara.sky` config**: Before creating a new file,
search for an existing `copy.bara.sky` file in the parent directory or up to 1-2
levels up (e.g. sibling to the `skills/` folder). If one exists, you should add
your new skill configuration to it by expanding the `origin_files` glob or
adding a new `dak_skills_sync_workflow` call. Otherwise, create a new file at
`{SOURCE_GP3_PATH}/copy.bara.sky` using the **Template** below.

1.5. **Register the skill build rule (Automated)**: The Copybara sync helper
automatically registers your skill in
`third_party/data_agent_kit/data_agent_common/skills/BUILD` during
synchronization. You do NOT need to edit this file manually.

1.6. **Verify Locally (Dry Run)**: * Run `copybara
{SOURCE_GP3_PATH}/copy.bara.sky sync_to_data_agent --dry-run` to verify that the
sync configuration compile checks and linters pass. * *Note: Because Copybara's
local client writes files to the destination during dry runs, this will create
synced files in your workspace under
`third_party/data_agent_kit/data_agent_common/skills/{skill_name}` and modify
`third_party/data_agent_kit/data_agent_common/skills/BUILD`. You should clean up
the created directory and revert the build file modification (e.g. using `rm -rf
third_party/data_agent_kit/data_agent_common/skills/{skill_name}` and `hg revert
third_party/data_agent_kit/data_agent_common/skills/BUILD`) before committing.*

1.7. **Create and Mail CL**:

````
 *   Create a CL containing only your local onboarding files
     (`copy.bara.sky`). **Do NOT commit any synced skill files or the
     modified build file.**
 *   Format the CL description using this template to bypass metadata
     checks:

     ```text
     GOOGLE:

     Onboard {PARTNER_TEAM_NAME} partner skill(s) to DAK

     This registers the {PARTNER_TEAM_NAME} partner skill(s) in DAK and sets up its local Copybara sync configuration.

     BUG={BUG_NUMBER}
     TAG=agy
     SKILL_EVALS_NOT_APPLICABLE=Only onboarding Copybara sync config
     NO_SKILL_EVALS_TESTED=Only onboarding Copybara sync config
     ```

 *   Add `DAK_REVIEWERS` as reviewers and mail the CL out.
````

### Stage 2: Post-Submission Tasks (Service Registration & Optional Initial Sync)
Once the onboarding CL (Stage 1) is submitted to Piper HEAD, the workflow **must
be registered** in the Copybara Service so that it runs automatically on future
commits.

2.1. **Register the Workflow in Copybara Service**:
     Run the following command to register the migration:
     ```bash
     /google/bin/releases/copybara/public/copybara/copybara service insert \
       --noprompt=true \
       piper://depot/google3/{SOURCE_GP3_PATH}/copy.bara.sky \
       {WORKFLOW_NAME}
     ```
     *Note: If you do not have permission to register it (e.g., you are not in
     the specified `owner_mdb`), ask a member of that group to run the
     command.*
2.2. **Trigger the Migration (Optional Initial Sync)**:
     The workflow will run automatically on any new commits.

Ask the user if they want to run the manual sync now (step 2.2.1 below):

     2.2.1. **Trigger the Migration**:
            Run the Copybara service trigger command to start the migration on CaaS at HEAD:
            ```bash
            /google/bin/releases/copybara/public/copybara/copybara service trigger \
              piper://depot/google3/{SOURCE_GP3_PATH}/copy.bara.sky \
              {WORKFLOW_NAME}
            ```
            This will trigger CaaS to run the sync workflow and handle the CL creation/submission automatically.

### Templates

#### Template: `copy.bara.sky`
Create (or update if already exists) `{SOURCE_GP3_PATH}/copy.bara.sky` using:

```python
"""Copybara configuration for syncing partner skills to DAK."""

load("//third_party/data_agent_kit/data_agent_common/skill_sync/copybara_helpers", "dak_skills_sync_workflow")

dak_skills_sync_workflow(
    origin_files = glob(
        ["{SOURCE_GP3_PATH}/**"],
        # Note: Do not copy-paste this list blindly. Scan your skill directory and
        # specify only the files that need to be excluded (e.g. internal tests,
        # evaluator configs, MDB group lists, internal READMEs, build files, etc.).
        exclude = [
            "**/copy.bara.sky",
            "**/BUILD",
            "**/METADATA",
            "**/OWNERS",
            # Add other specific files/globs to exclude here
        ],
    ),
    author = "{PARTNER_TEAM_NAME} Team <no-reply@google.com>",
    workflow_name = "{PARTNER_TEAM_NAME}_dak_skills_sync",  # MUST be globally unique across all CaaS migrations in Google
    owner_mdb = "{PARTNER_MDB_GROUP}",
    contact_email = "{PARTNER_EMAIL}",
    destination_skills_globs = ["{PARTNER_SKILL_NAME_PREFIX}/**"],  # e.g., ["gcs_transfer/**"] or ["gcs_**"]
    # Optional: reviewers = {DAK_REVIEWERS},
    # Optional: Pass custom transformations (e.g. to rewrite absolute google3 imports to relative imports):
    # transformations = [
    #     core.replace(
    #         before = """# pylint: disable=g-import-not-at-top
    # try:
    #   from google3.path.to.my.original.package.scripts import ${module}
    # except ImportError:
    #   import ${module}  # type: ignore
    # # pylint: enable=g-import-not-at-top""",
    #         after = "from . import ${module}",
    #         multiline = True,
    #         repeated_groups = True,
    #         regex_groups = {
    #             "module": "[a-zA-Z0-9_]+",
    #         },
    #     ),
    # ],
)
```
