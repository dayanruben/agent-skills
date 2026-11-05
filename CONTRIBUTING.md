# Contributing

Create one capability per directory under `skills/`, following the [Agent Skills specification](https://agentskills.io/specification). Start with `SKILL.md`:

```yaml
---
name: example-capability
description: Explain the task this skill performs and when an agent should select it.
license: MIT
---
```

Below the frontmatter, write the purpose, essential workflow, output expectations, missing-input behavior and a realistic example. Add optional `references/`, `scripts/`, `assets/` and `agents/openai.yaml` only when useful. Keep relative links inside the skill and include required license notices. Avoid credentials, internal data, blanket execution authority, generic boilerplate and unnecessary dependencies.

Attribute sources and date-sensitive claims. Prefer primary documentation; do not reproduce copyrighted articles. Test scripts in isolation and explain dependencies and side effects. Read-only audits should not run the project under review. Describe evidence and limitations rather than claim complete safety.

Use English throughout. Follow [the authoring guide](docs/authoring.md) and keep the standard `skills/<name>/SKILL.md` layout discoverable by the skills.sh CLI. Do not hide catalog skills with `metadata.internal`, require a proprietary agent, or depend on another locally installed skill without documenting that requirement.

Update the README catalog. Run the validation and CLI discovery commands in [README.md](README.md), then `git diff --check`. Python updates must refresh the version and compatible wheel hashes together using PyPI's SHA-256 digests; npm updates must include `package-lock.json`. Never remove integrity checks to get CI green. Review Dependabot changes for lock coverage and verified upstream action commits. Do not run untrusted updates with privileged credentials.

Sign every commit using your configured signing identity (`git commit -S`), verify it locally with `git verify-commit HEAD`, and check GitHub's verification status after pushing. Do not disable signing or create a replacement identity to satisfy a check. Repository rules enforce signed commits on all branches.

Open a focused pull request. A maintainer should review instructions, references, scripts, sources, permissions and network behavior before adoption. Packaging validation cannot certify safe behavior. Keep branch protections and required checks intact.
