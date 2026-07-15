# OGHO template compliance workflow

This repository hosts the reusable GitHub Action that checks Oracle repositories for compliance with the repository requirements defined by [`oracle/template-repo`](https://github.com/oracle/template-repo).

It does not maintain copies of the repository templates. The action reads the canonical `SECURITY.md` from `oracle/template-repo` at runtime, and this repository's test workflow checks the validator against a fresh checkout of that repository.

## Add the workflow to a repository

Create `.github/workflows/ogho-template-compliance.yml` in the repository to validate:

```yaml
name: OGHO template compliance

on:
  pull_request:
  merge_group:

permissions:
  contents: read

jobs:
  validate:
    name: Validate repository template
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v7

      - name: Run OGHO template checks
        uses: oracle-samples/ogho-compliance/.github/actions/ogho-template-check@<FULL_COMMIT_SHA>
```

Replace `<FULL_COMMIT_SHA>` with the full SHA of an approved commit from this repository. Pinning the action prevents unreviewed changes from altering the code executed by the workflow.

The action checks the repository name and default branch, required root files, license format, required README and contributing-guide sections, and the canonical security policy. It reports failures as GitHub annotations and in the job summary.

## Action inputs

Most workflows do not need to set inputs.

| Input | Default | Purpose |
| --- | --- | --- |
| `path` | `.` | Repository path to inspect, relative to `GITHUB_WORKSPACE`. |
| `repository-name` | GitHub event metadata | Override used for local tests or nonstandard events. |
| `default-branch` | GitHub event metadata | Override used for local tests or nonstandard events. |
| `contributing-policy` | `optional` | Use `required` to require a local guide or `disabled` to skip the check. |

For organization-wide ruleset configuration, rollout guidance, and troubleshooting, see the [OGHO template compliance workflow guide](docs/ogho-template-compliance-workflow.md).

## License

Copyright (c) 2026 Oracle and/or its affiliates.

Released under the Universal Permissive License v1.0 as shown in [LICENSE.txt](LICENSE.txt).
