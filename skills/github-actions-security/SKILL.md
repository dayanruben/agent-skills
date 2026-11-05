---
name: github-actions-security
description: "Audit and harden GitHub Actions against malicious pull requests, dependency compromise, credential theft, and unsafe release workflows. Use for an Actions security review or authorized workflow hardening."
license: MIT
metadata:
  author: dayanruben
  version: "1.1.0"
---

# GitHub Actions security

## When to apply

Use for an explicitly requested Actions security audit, a workflow review focused on trust boundaries, or authorized CI hardening. An ordinary code change does not by itself call for a repository-wide audit.

## Workflow

Turn an Actions security request into evidence-backed findings and, when requested, focused fixes. The threat model is an outside attacker controlling contributions or a supply-chain dependency. This skill does not establish protection against a compromised maintainer.

1. **Establish scope.** Read repository instructions and inspect Git status. Identify repository, ref, commit, fork/upstream relationship, and whether the request is an audit or includes fixes. Preserve unrelated work. Start with static inspection; do not run project code, install dependencies, dispatch privileged workflows, or retrieve secret values just to audit them.
2. **Map trust boundaries.** Inventory workflows, reusable workflows, local actions and the scripts they call. For each job, record triggers, attacker-controlled inputs, checked-out ref, runner, effective token permissions, secrets/OIDC, caches, artifacts, and publication/deployment effects. Follow indirect execution through installers, build tools, actions and artifact consumers. Record inaccessible dependencies and settings as unknown.
3. **Review relevant controls.** Use [the control guide](references/controls.md), covering all nine areas when reviewing a whole repository. Use [sources and platform caveats](references/sources.md) to verify changing syntax, feature availability and tool behavior. Separate observable risks from recommendations and controls that do not apply.
4. **Apply authorized fixes.** Prefer small changes that preserve intended CI and release behavior. Verify action commits against upstream history before pinning. Keep fork validation separate from upstream publication. Use existing authorization; the skill grants no extra authority to change organization policies, credentials, runner infrastructure, or production access. Do not bypass review, weaken checks, force-push, or enable publication in validation-only forks.
5. **Validate without exposing privileged context.** Run available `actionlint` and `zizmor --strict-collection --persona=pedantic .` against the scoped repository, plus relevant existing checks. Review coverage and tool versions: offline zizmor skips online provenance audits. If online checks are authorized, pass a suitably scoped token through the environment, never print it or embed it in command arguments. Inspect scripts and reusable workflows manually; linting alone does not cover them. Do not install tools silently. Recheck the diff and Git status, and distinguish local validation from exact-commit remote CI results.
6. **Report the result.** Identify scope/ref/SHA; list findings by severity with `path:line`, attacker input, execution path, privilege exposed, and concrete mitigation. Include changes, checks and coverage, remaining unknowns, and settings requiring a maintainer action. An unavailable check is unknown. A clean bounded scan supports only “no findings in the inspected scope.”

**Example request:** “Audit this repository's Actions and fix issues within the existing workflow scope.”

**Expected behavior:** Find a privileged workflow executing a PR-head build script; explain how the fork controls that script and which job credentials it can reach; move validation to a restricted PR job; preserve a necessary metadata-only privileged task; report validation and unreadable repository settings. Do not trigger a real deployment to prove the fix.
