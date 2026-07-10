# Codelab: Onboarding Your Skill to the Data Agent Kit (DAK)

Welcome! This guide will help you integrate your team's domain-specific AI agent
skills into the **Data Agent Kit (DAK)**.

### High-Level Architecture

```mermaid
graph TD
    subgraph level1 [Level 1: Partner Source (google3)]
        YourRepo["Your Team's google3 Source Directory<br/>//depot/google3/path/to/your/skills/your-skill"]
    end

    subgraph level2 [Level 2: DAK Core (google3)]
        SkillsDir["DAK Shared Skills Directory<br/>//third_party/data_agent_kit/data_agent_common/skills"]
    end

    subgraph level3 [Level 3: DAK Downstream Bundles]
        VSIX["DAK IDE Extension<br/>VSIX Bundle"]
        GitHubRepo["DAK Starter Pack GitHub Repo<br/>gemini-cli-extensions/data-agent-kit-starter-pack"]
    end

    %% Data Flows
    YourRepo -- "Automated Copybara Sync<br/>(CaaS Workflow)" --> SkillsDir
    SkillsDir -- "Weekly Extension Release" --> VSIX
    SkillsDir -- "Weekly Release Export" --> GitHubRepo
```

---

## Onboarding Overview

The onboarding process registers your skill in the DAK repository and sets up
automated syncs so that any future changes you make to your skill files are
automatically imported to DAK.

Onboarding consists of two stages:

1.  **Stage 1: Config CL**: Create a Copybara configuration file
    (`copy.bara.sky`) in your skill directory that calls the
    `dak_skills_sync_workflow` Starlark helper function (providing your team
    name, MDB group, contact email, and destination skills path prefix). Submit
    this configuration to google3.
2.  **Stage 2: Service Registration**: Once the config CL is submitted to Piper
    HEAD, the workflow must be registered in the Copybara Service (CaaS) using
    the `copybara service insert` command. CaaS will then run the sync to DAK
    whenever you submit changes to your skill.

> [!NOTE]
> **Weekly Release Sync**: Once your skill is successfully synchronized into
> google3 (`data_agent_common/skills`), it is packaged into the IDE extension
> and exported to the public GitHub repository
> (`data-agent-kit-starter-pack`) as part of DAK's weekly release process. These
> weekly releases are gated by post-submit evaluation runs to ensure stability.

---

## Under the Hood: How the Sync Workflow Works

To keep integration maintenance low, DAK uses a custom Copybara helper
(`dak_skills_sync_workflow`) to automate the skill registration process during
synchronization:

1.  **Workflow Registration**:
    The migration is registered with Copybara-as-a-Service (CaaS) using the
    `copybara service insert` CLI command. CaaS then manages and schedules the
    migration in the background.
2.  **Dynamic Skill Discovery**:
    During sync runs, the helper scans your source directory for any `SKILL.md`
    files. For each skill found, it:
    *   Normalizes the directory name (converting hyphens to underscores) to
        ensure valid Python import package names.
    *   Copies all skill files (markdown, scripts, resources) under the central
        DAK skills path:
        `third_party/data_agent_kit/data_agent_common/skills/{normalized_skill_name}`.
3.  **BUILD Integration**:
    The helper automatically updates
    `third_party/data_agent_kit/data_agent_common/skills/BUILD` using buildozer,
    adding your skill's target name to the central list of partner skills. This
    declares the `agent_skill` build rules and generates the validation tests
    automatically.
4.  **Downstream Packaging**:
    Once the files are synced to `data_agent_common`, they are bundled into the
    IDE extension VSIX and pushed to the public GitHub repository as part of
    DAK's weekly release process.

---

## Sync Schedules & Initial Sync Options

Understanding how and when your skills sync to DAK is important for managing
your releases:

*   **Workflow Activation**: Once your Stage 1 config CL is submitted to Piper
    HEAD, the workflow must be registered in CaaS (typically via the command:

    ```bash
    /google/bin/releases/copybara/public/copybara/copybara service insert \
      --noprompt=true \
      piper://depot/google3/path/to/copy.bara.sky \
      workflow_name
    ```

    Once registered, it is active.
*   **Change-Driven Syncing**: The workflow runs on an automated schedule that
    monitors your source directory. **It only triggers a sync run when a new
    change is committed to your source directory.**
*   **The Initial Sync Choice**: Because the sync is change-driven, your
    existing skill files will **not** be imported automatically when the
    workflow is first activated. To perform the initial sync, you have two
    choices:
    *   **Option A: Wait for Next Commit**: Do nothing. The next time you submit
        a change to your skill's source directory, CaaS will trigger and perform
        the import automatically.
    *   **Option B: Force Immediate Sync**: If you want to import your existing
        skill files immediately, ask your AI assistant to run the manual sync
        (see the prompt in the next section). The assistant will trigger the
        migration, format the CL, and mail it to you.
*   **Monitoring Migration Status**: You can view registration status, history,
    and log files for your migrations on the
    [Copybara UI (go/copybara-ui)](http://go/copybara-ui) dashboard.

---

## AI-Assisted Onboarding (Recommended)

The easiest way to onboard your skill is using an AI coding assistant (like
Jetski, Gemini, or Antigravity) that has the DAK Partner Onboarding skill
loaded.

Simply prompt the assistant with this message:

> Please onboard a new partner skill following the instructions in
> file:///google3/third_party/data_agent_kit/data_agent_common/skill_sync/skills/partner_skill_onboarding/SKILL.md

### What you need to provide:
When prompted by the assistant, provide these details:

*   **Skill Source Path**: The absolute google3 path to your skill source files
    (e.g.,
    `google3/java/com/google/android/apps/gcs/agent/skills/gcs_transfer`).
*   **MDB Group**: Your team's MDB group (for ownership & notifications).
*   **Contact Email**: Your team's mailing list or contact email.
*   **Bug Number**: The Buganizer bug tracking this onboarding.

The assistant will automatically scan your imports, generate the `copy.bara.sky`
file, run dry-run verification, and create the onboarding CL for you.
