# Controls for outside threats

Use the sections that match the workflow. For a repository-wide audit, mark every area as reviewed, not applicable, or unknown, with evidence. Consult [maintained sources](sources.md) before depending on preview features or version-specific behavior.

## 1. Action and workflow dependencies

- Inspect every remote `uses`, including reusable workflows and nested composite actions. Prefer full verified commit SHAs where dependency lockfiles are unavailable or do not cover a reference. Pin container images by digest. A direct SHA does not freeze nested `uses`, Docker base images, package downloads or a wrapper's downloaded CLI.
- Where supported, evaluate GitHub workflow dependency lockfiles with upstream identity verification and transitive action coverage. Onboard shared-workflow repositories first. Generate and verify with official tooling; review changed commits and repository identities. Do not hand-edit lockfiles, assume they cover reusable-workflow calls or containers, or enforce them before all targeted workflows are covered.
- Resolve a requested version in the actual upstream and verify commit reachability from its history. An API lookup returning a commit through an upstream URL is insufficient: GitHub fork networks can expose fork-only commits there. An immutable malicious commit is still malicious. Never invent a SHA or commit documentation placeholders.
- Keep reviewed version comments and a dependency update process. Check advisory coverage for the chosen reference format; version update PRs alone do not guarantee vulnerability alerts. Do not mechanically replace a valid enforced lockfile with inline pins.

## 2. Tokens, secrets and publication

- Prefer workflow-level `permissions: {}` and explicit minimum grants per job. Check effective permissions, reusable workflow inheritance, PAT/App tokens and `secrets: inherit`; reducing `GITHUB_TOKEN` does not restrict independent credentials. Use `persist-credentials: false` unless later authenticated Git operations are required.
- Grant `id-token: write` only to a job needing OIDC. Any step in that job can request a token: an environment variable scoped to publishing does not isolate hostile build/install steps. Constrain provider trust to the intended repository, workflow/ref or protected environment, and audience.
- Separate building from publishing. Keep publishing credentials out of the build job; use a minimal publish job consuming verified outputs without project hooks or newly downloaded unreviewed code. Check environment protections and who may approve them. Without settings access, do not claim enforcement.
- In compatibility-validation forks, preserve validation while preventing package/release publication, container pushes and documentation deployments. Preserve upstream releases in the intended trusted context.

## 3. Privileged triggers and artifacts

- Prefer `pull_request` for untrusted contributions with restricted permissions and no secrets. Check actual fork/private-repository settings rather than assuming defaults. Inspect `pull_request_target`, `workflow_run`, comments, dispatches and reusable entrypoints for indirect untrusted execution.
- In privileged contexts, do not check out or execute a PR head, its scripts, dependencies, local actions or artifact executables. A base checkout helps only if later steps also avoid attacker-controlled execution. Do not opt out of checkout's unsafe-PR protections as a fix.
- A separate privileged workflow is not automatically safe. Bind downloads to the triggering run ID; verify repository, workflow identity, event, ref/head SHA, conclusion and artifact identity against the intended operation. Success alone is insufficient. Validate file names, size limits and schema; reject extraction traversal and unsafe links. Never source, eval or execute untrusted reports.
- Publish only outputs from the intended trusted build/ref; download integrity does not make a fork artifact releasable. Minimize uploads and exclude credentials, workspace internals and secret-bearing files.

## 4. Expression and command injection

Trace PR/issue text, branch names, commit messages, workflow inputs and downloaded data into `run`, script inputs, shell evaluation and command files. Trust depends on who controls a value, not a `github.event` prefix.

Pass data through an environment variable and quote its use:

```yaml
- name: Read the title as data
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: printf '%s\n' "$PR_TITLE"
```

Do not substitute the expression directly into shell or `actions/github-script` source. In JavaScript, read `context.payload` or `process.env`. Avoid `eval`, input passed to `bash -c`, and unsafe argument construction. Validate data written to `GITHUB_ENV`, `GITHUB_OUTPUT` and `GITHUB_PATH`; an `env:` binding does not make subsequent command-file writes safe. Use fixed output formats and handle multiline data correctly. Do not execute an attacker's payload to demonstrate injection.

## 5. Cache boundaries

- Map writing events/refs and privileged consumers, including setup-action automatic caches. Scope is a service property; key prefixes and lockfile hashes are not access control. Ordinary PR merge-ref caches are not restorable by the base branch; fork PRs can read eligible base caches. Never cache secrets.
- Check current defaults and explicit `cache-mode` overrides. Where supported, cap untrusted jobs at `read` or `none` and use `none` for clean release jobs. Write-capable low-trust overrides can reopen a protected boundary. Verify limits also apply to reusable workflows.
- Without service-side controls, remove unsafe producers/consumers and explicitly disable relevant setup-action caches. Restore-only steps express intent but do not constrain malicious code holding a separate cache service token. Avoid executable caches of uncertain provenance in publishing jobs.

## 6. Runners

- Prefer GitHub-hosted runners for outside contributions. First-contributor approval, labels and actor-name checks do not establish durable isolation.
- If self-hosted hardware is necessary, inspect group/workflow restrictions, untrusted scheduling, persistent workspaces, credentials, sibling jobs, metadata endpoints and network reach. Use isolated ephemeral hosts with teardown/reimaging after each job. Deregistration or workspace deletion does not establish host cleanup.
- Separate untrusted public jobs from private workloads and production networks. Mark unverifiable infrastructure controls unknown. Do not reconfigure live runners as a YAML-audit side effect.

## 7. Dependency intake

- Use deterministic installs with committed lockfiles and verification where supported. Inspect registry overrides, Git/URL/path dependencies, install hooks and build plugins. For Gradle, examine dependency locking, verification metadata and wrapper integrity rather than applying npm commands.
- Keep credentials out of installation. Disable lifecycle scripts where compatible and review exceptions; preserve needed native builds with a narrow allowlist instead of silently breaking CI.
- Assess release-age controls at resolution and in update bots. Frozen installs consume a lockfile and do not reapply a resolution cooldown. Verify package-manager support and units; do not delay urgent security fixes with an arbitrary universal waiting period.

## 8. Downloaded scripts and uploaders

- Find pipe-to-shell installers, downloaded executables and tools fetched inside actions. Pin payload versions; verify integrity with a reviewed committed digest or authenticated signatures using an independently trusted signer/key. Checksums fetched from the same mutable location do not independently authenticate a compromised distribution.
- Inspect wrapper defaults and verification bypass inputs: an action SHA may still fetch a `latest` CLI. Keep verification enabled and downloads outside privileged build contexts where possible. HTTPS and version-looking URLs alone do not establish integrity.

## 9. Network access and residual risk

- Inventory required destinations before proposing egress enforcement. Begin with observable auditing, then a maintained narrow allowlist and denial alerts. Verify untrusted jobs cannot broaden enforcement; account for cloud metadata, internal services and production networks. Do not silently install an egress agent or assume a planned feature exists.
- Allowed services and public workflow logs remain exfiltration channels. Filtering complements least privilege; it cannot make secret-bearing execution of hostile code safe.
- State residual risks: compromised maintainers, unknown dependencies, inaccessible settings and runtime behavior exceed what static review proves. Do not present these controls as a complete security guarantee.
