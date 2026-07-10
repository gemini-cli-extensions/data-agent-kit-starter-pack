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
3. **Label & Import**: `release-please` opens a version bump PR on GitHub (`data-agent-kit-starter-pack`). Attach label `copybara:import-manual` and import the PR into Piper via Copybara.
4. **Submit Import CL**: Submitting the imported Piper CL syncs the version bump back to GitHub, merging and closing the `release-please` PR.
5. **Tag & Publish**: Create and publish the GitHub release tag `v<X.Y.Z>`.
6. **Downstream Upgrade**: Merge the automated downstream upgrade PR in `GoogleCloudPlatform/data-agent-kit`.

---

## Step 1: Determine Release Version & Create Force Release CL in Piper

1. **Ask the user** for the exact release version number they want to publish (e.g., `0.6.1`).
2. Once target version `X.Y.Z` is confirmed, create a Piper changelist where you update the release tracking comment inside `third_party/data_agent_kit/data_agent_common/README.md` right below `<!-- {x-release-please-end} -->`:
   ```markdown
   <!-- {x-release-please-end} -->
   <!-- release-version-force-update: X.Y.Z -->
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

3. Verify on `https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commits/main` that the commit has landed.

---

## Step 3: Monitor `release-please` PR & Copybara Import to Piper

Once the `chore: force release X.Y.Z` commit lands on GitHub `main`:
1. **Release Please Bot Action**: The `release-please` bot detects `Release-As: X.Y.Z` and automatically opens a version upgrade Pull Request on `data-agent-kit-starter-pack` (titled `chore: release X.Y.Z`). This PR updates version numbers across `package.json`, `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, and `CHANGELOG.md`.
2. **Automatic Copybara PR Import**: Copybara detects the newly created `release-please` Pull Request and automatically imports it into Google3 within 5–10 minutes, generating a corresponding **Piper CL** containing the version upgrades. Or, if you want to trigger the inbound import workflow immediately without waiting:

```bash
copybara service trigger \
  piper://depot/google3/third_party/data_agent_kit/data_agent_common/copy.bara.sky \
  data_agent_common_skills_github_pr_to_piper \
  --worker-flags
```

---

## Step 4: Review and Submit the Piper Import CL

1. Locate the imported Piper CL in Google3 (`//depot/google3/third_party/data_agent_kit/data_agent_common/`) corresponding to the version upgrade.
2. Verify that presubmits pass (`hg presubmit --detach` / Sponge tests).
3. **Tell the user** to review and **submit** this imported Piper CL.

Submitting this CL in Piper establishes the new release version (`X.Y.Z`) as the official Source of Truth in Google3.

---

## Step 5: Verify Automatic Merge on GitHub

After the Piper import CL from Step 4 is submitted:
1. Trigger or wait for Copybara postsubmit export (`piper_sot_to_github`) to sync the submitted version upgrade commits from Piper back to GitHub `main`.
2. Because the exact version upgrade changes and diff are now present on `main`, GitHub automatically marks the original `release-please` Pull Request as **Merged** (and closes it).

---

## Step 6: Create and Publish GitHub Release Tag (`vX.Y.Z`)

Instruct the user to navigate to the GitHub Releases page:
`https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/releases`

1. Click **Draft a new release**.
2. Click **Choose a tag**, type `vX.Y.Z` (e.g., `v0.6.1`), and select **Create new tag: vX.Y.Z on main**.
3. Set the **Release title** to `vX.Y.Z`.
4. Copy and paste the changelog section generated by `release-please` (or click **Generate release notes**).
5. Click **Publish release**.

---

## Step 7: Verify and Merge Downstream PR in `GoogleCloudPlatform/data-agent-kit`

Publishing the release tag (`vX.Y.Z`) on `data-agent-kit-starter-pack` triggers a downstream automated workflow that opens a dependency upgrade Pull Request in the primary parent repository:
`https://github.com/GoogleCloudPlatform/data-agent-kit`

1. Tell the user to go to the Pull Requests tab on `https://github.com/GoogleCloudPlatform/data-agent-kit/pulls`.
2. Locate the automated PR updating the starter pack dependency to version `vX.Y.Z`.
3. Verify CI checks pass, then **approve and merge** the Pull Request to complete the end-to-end release lifecycle.
