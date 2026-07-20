---
name: gcloud-auth-verification
description: Guidelines for identifying and resolving missing Google Cloud authentication
  and Application Default Credentials (ADC). Use this skill if `gcloud`, `bq`, `dataform`,
  or Python libraries return authentication errors.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

# Handling Authentication Issues

## Common Error Messages

1.  **gcloud/bq CLI**:
    -   `ERROR: (bq) You do not currently have an active account selected.`
    -   `No credentialed accounts.`
    -   `Configuration error: No account is currently active.`
2.  **Execution Failures (Python/Notebooks)**:
    -   `google.auth.exceptions.DefaultCredentialsError: Could not automatically
        determine credentials.`
    -   `Forbidden: 403 Access Denied` (when it's clearly an auth issue).

## Verification Step

Before asking the user to log in, independently verify the authentication status
by running: `gcloud auth list` * If the output contains `No credentialed
accounts.`, proceed to the **Corrective Action** steps below. * If an account
*is* listed but the user still receives a `403 Access Denied` error, the issue
is likely **IAM permissions** (e.g., missing BigQuery roles) on their active
account, rather than missing authentication. In this case, investigate the
permissions rather than asking them to log in again.

## Corrective Action

When missing credentials are confirmed, **DO NOT** attempt to fix the
credentials via code or alternative tools. Credentials must be established by
the user.

**Stop and ask the user to run the following commands in their terminal:**

1.  **To authenticate the gcloud CLI**: `gcloud auth login`

2.  **To set up Application Default Credentials (ADC)** (required for BQ CLI AND
    most libraries/notebooks): `gcloud auth application-default login`

## Post-Login Verification

After the user confirms they have logged in, verify with: `gcloud auth list`
Then proceed with the original task.
