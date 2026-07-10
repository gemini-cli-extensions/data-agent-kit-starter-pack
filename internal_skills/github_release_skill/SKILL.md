---
name: github-release-skill
description: Comprehensive internal guide and workflow for oncall engineers to synchronize Data Agent Kit (data_agent_common) changes to GitHub, trigger release-please version updates, submit resulting Piper CLs, publish GitHub releases, and merge downstream repository updates.
---

# Data Agent Kit (`data_agent_common`) GitHub & Piper Release Skill

This skill assists oncall engineers with executing the end-to-end release lifecycle for `data_agent_common` across Google3 Piper and public GitHub repositories (`data-agent-kit-starter-pack` and `data-agent-kit`) using Piper as the single Source of Truth.

## Overview of Release Flow

The release process coordinates synchronization and versioning cleanly from Google3:
1. **Force Release CL in Piper**: Create a `Release-As: v<X.Y.Z>` commit in Piper updating the release tracking comment in `README.md`.
2. **Sync to GitHub**: Submit the CL and sync to GitHub (`copybara service trigger`) to wake up `release-please`.
3. **Automatic Import**: `release-please` opens a version bump PR on GitHub (`data-agent-kit-starter-pack`), which Copybara automatically imports into Piper.
4. **Submit Import CL**: Submitting the imported Piper CL syncs the version bump back to GitHub, merging and closing the `release-please` PR.
5. **Tag & Publish**: Create and publish the GitHub release tag `v<X.Y.Z>`.
6. **Downstream Upgrade**: Merge the automated downstream upgrade PR in `GoogleCloudPlatform/data-agent-kit`.

## Goal-Oriented Agent Behavior & Status Checklist

When executing this skill as an agent:
- **Always display a 7-Step Status Checklist** formatted with clear status indicators (`[x]` Done, `[>]` Current / Action Required, `[ ]` Pending) so the user knows exactly what is completed, what requires their check or approval, and what remains.
- Maintain proactive, goal-oriented momentum across all 7 steps.
- At checkpoints requiring human approval and submission (**Step 2** and **Step 4**), explicitly instruct the user: *"Please review and submit [CL link]. Once submitted, let me know right away so I can immediately execute the next Copybara command and guide us through the remaining steps."*
- Never stop or leave the user guessing what happens next; drive the release workflow continuously to completion.

---

## Step 1: Determine Release Version & Create Force Release CL in Piper

1. **Ask the user** for the exact release version number they want to publish (e.g., `0.6.1`).
2. Once target version `X.Y.Z` is confirmed, create a Piper changelist where you update or rotate the release tracking comment inside `third_party/data_agent_kit/data_agent_common/README.md` right below `<!-- {x-release-please-end} -->` (e.g. `<!-- github-release-force: X.Y.Z -->` or `<!-- release-version-force-update: X.Y.Z -->`) to guarantee a non-empty file diff when exported to GitHub:
   ```markdown
   <!-- {x-release-please-end} -->
   <!-- github-release-force: X.Y.Z -->
   ```
3. Format the Piper CL commit description so that when exported to GitHub, the `Release-As: X.Y.Z` trailer instructs the `release-please` bot to cut the release:

```text
chore: force release X.Y.Z

Release-As: X.Y.Z

GOOGLE:
TAG=agy
```

---

## Step 2: Submit the Force Release CL & Sync to GitHub

1. **Ask the user** to review, obtain approval, and **submit** the force release Piper CL created in Step 1.
2. Once submitted, trigger the Copybara backend service to push the submitted commit (`Release-As: X.Y.Z`) directly to the public GitHub repository (`gemini-cli-extensions/data-agent-kit-starter-pack`):

```bash
copybara service trigger \
  piper://depot/google3/third_party/data_agent_kit/data_agent_common/copy.bara.sky \
  data_agent_common_skills_postsubmit_piper_to_github \
  --worker-flags
```

> [!NOTE]
> Do **NOT** include `--squash` so that individual commit messages, including the `Release-As: X.Y.Z` trailer, are preserved on the GitHub `main` branch.

> [!TIP]
> **Automatic Export Merging**: When you trigger `data_agent_common_skills_postsubmit_piper_to_github`, Copybara opens an export Pull Request on GitHub and **automatically merges it onto `main`** as soon as checks pass. You do **not** need to manually run `gh pr merge` on this PR. Simply wait a few moments and verify on `commits/main` that your commit has landed automatically.

3. Verify on `https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commits/main` that the commit has landed automatically.

---

## Step 3: Monitor `release-please` PR & Copybara Import to Piper

Once the `chore: force release X.Y.Z` commit lands on GitHub `main`:
1. **Release Please Bot Action**: The `release-please` bot detects `Release-As: X.Y.Z` and automatically opens a version upgrade Pull Request on `data-agent-kit-starter-pack` (titled `chore: release X.Y.Z`). This PR updates version numbers across `package.json`, `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, and `CHANGELOG.md`.
2. **Automatic Copybara PR Import**: Copybara detects the newly created `release-please` Pull Request (`pull_request.opened` event) and automatically imports it into Google3 within 5–10 minutes (`EVENT_BASED`).

### Safe Review Gate (`go/copybara-safe-review`)
Because `release-please[bot]` is not a Googler (`@google.com`) and its new PR initially has no approvals on GitHub, Copybara's mandatory security policy intercepts the import and creates a **Gerrit Safe Review (`copybara-safe-internal-review.git.corp.google.com`)** instead of generating an immediate Critique CL.

To release the Safe Review and generate your Critique changelist (`http://cl/...`), use either method below:
* **Method 1 (Preferred - Gerrit Safe Review)**: Copybara notifies `safe_reviewers` via email with a Gerrit Safe Review link. Click **Code-Review +2 / Submit** directly inside Gerrit (`copybara-safe-internal-review.git.corp.google.com`) to instantly mark the check passed and release the Critique CL (`http://cl/...`). This is safest because the GitHub PR remains completely unapproved on GitHub until Copybara syncs the submitted change, eliminating any risk of premature merges on GitHub.
* **Method 2 (GitHub Approval)**: If a Googler (`@google.com`) approves the PR directly on GitHub (`pull_request_review.submitted`), Copybara re-evaluates the PR on its next cycle (~5–10 minutes) and generates the Critique CL (`http://cl/...`).

---

## Step 4: Review and Submit the Piper Import CL

1. Locate the imported Piper CL (`http://cl/...`) in Critique corresponding to the version upgrade. Note that the imported CL is owned by the automated service account (`copybara-worker@copybara-worker`).
2. **Adding Yourself to Reviewers**: Because `copybara-worker` owns the CL, the **LGTM** (Approve) button in Critique is disabled for non-owners until you explicitly add your user account (`e.g. ellurubharath`) to the `R=` (Reviewers) list in Critique (`+ Add Reviewer`). Once added, click **LGTM** (Approve).
3. **Two-Party Review Policy**: For automated bot imports, Google3 Two-Party Review rules mandate **two distinct human Googlers** combined across GitHub and Critique. If Googler 1 (`e.g. ellurubharath`) approved on GitHub or Gerrit, Copybara requires an additional `LGTM` from **Googler 2** (`e.g. danielheyman`, `girishduvuru`, or `snehamitshah`) in Critique before submitting.
4. **Automated Submission (`auto-submit`)**: Because `copybara-worker` owns the CL, the **SUBMIT** button in Critique is disabled for non-owners. Once the CL receives the required `LGTM` from a Source of Truth reviewer and passes presubmits, Copybara's automated polling cycle (~5–10 minutes) **automatically submits the CL** in Piper!

Submitting this CL in Piper establishes the new release version (`X.Y.Z`) as the official Source of Truth in Google3.

---

## Step 5: Verify Automatic Merge on GitHub

After the Piper import CL (`Step 4`) is automatically submitted by Copybara:
1. **Trigger Postsubmit Export**: Because `copy.bara.sky` configures `triggering = "MANUAL"` for postsubmits, you MUST manually trigger `copybara service trigger` to export the submitted version upgrades to GitHub `main`:

```bash
copybara service trigger \
  piper://depot/google3/third_party/data_agent_kit/data_agent_common/copy.bara.sky \
  data_agent_common_skills_postsubmit_piper_to_github \
  --worker-flags
```

2. **Automatic Export Merging**: Copybara opens an export Pull Request on GitHub and **automatically merges it onto `main`** as soon as status checks pass (`pull_request.closed/merged`). No manual `gh pr merge` is required.
3. **PR #152 Auto-Closure**: Because the exact version upgrade changes and diff are now present on `main`, GitHub automatically marks the original `release-please` Pull Request (`#152`) as **Merged** (and closes it).

---

## Step 6: Create and Publish GitHub Release Tag (`X.Y.Z`)

Instruct the user to navigate to the GitHub Releases page:
`https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/releases`

1. Click **Draft a new release**.
2. Click **Choose a tag**, type `X.Y.Z` (e.g., `0.6.1` — **without a leading `v`** because `release-please-config.json` sets `"include-v-in-tag": false`), and select **Create new tag: X.Y.Z on main**.
3. Set the **Release title** to `vX.Y.Z` (e.g., `v0.6.1` — **with a leading `v`**).
4. Copy and paste the changelog section generated by `release-please` (or click **Generate release notes**).
5. Click **Publish release**.

---

## Step 7: Verify and Merge Downstream PR in `GoogleCloudPlatform/data-agent-kit`

Publishing the release tag (`vX.Y.Z`) on `data-agent-kit-starter-pack` triggers a downstream automated workflow that opens a dependency upgrade Pull Request in the primary parent repository:
`https://github.com/GoogleCloudPlatform/data-agent-kit`

1. Tell the user to go to the Pull Requests tab on `https://github.com/GoogleCloudPlatform/data-agent-kit/pulls`.
2. Locate the automated PR updating the starter pack dependency to version `vX.Y.Z`.
3. Verify CI checks pass, then **approve and merge** the Pull Request to complete the end-to-end release lifecycle.
