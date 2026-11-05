# Agent Skills

Reusable [Agent Skills](https://agentskills.io/specification) for software engineering workflows. Each skill is self-contained and source-attributed. Review it as executable guidance before use.

**Other language:** [Português](README.pt-BR.md)

## Catalog

| Skill | Use it for |
| --- | --- |
| [github-actions-security](skills/github-actions-security/SKILL.md) | Audit and harden GitHub Actions against outside threats across nine control areas, with English and PT-BR guidance. |

## Use a skill

Review the skill and its supporting files at a specific commit before installing it. A skill can suggest commands and external actions; its presence does not grant credentials or additional authorization.

Clone this repository and copy the complete `skills/<name>/` directory to your agent's supported skill location. Preserve references and license. For Codex, a user-level installation can use `~/.agents/skills/<name>/`; consult [the current documentation](https://developers.openai.com/codex/skills) for other scopes and discovery behavior. Other agents have their own setup. Storage in this repository alone does not activate a skill.

Example invocation after setup:

```text
Use $github-actions-security to audit this repository's workflows.
Report findings with file/line evidence and propose focused fixes.
```

## Add future skills

Add `skills/<name>/SKILL.md` with standard YAML frontmatter and focused instructions. Keep optional references, scripts and assets inside that directory. Update both catalogs and follow [CONTRIBUTING.md](CONTRIBUTING.md) for validation and review. Do not include credentials, private operational data, automatic installation hooks or unreviewed code execution.

## Validation and repository security

```sh
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python --require-hashes --no-deps --only-binary=:all: -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/zizmor --offline --strict-collection --persona=pedantic .
```

The validator checks manifests, optional Codex UI metadata and inline Markdown file links, including self-contained skill references. It does not execute skill scripts, fetch external links, assess security claims, or replace human review. Hash-locked development tools support CPython 3.13 on Linux x86_64 and macOS arm64. Local offline zizmor omits provenance audits; CI uses a read-only job token for online checks in a separate job that runs no repository scripts.

CI uses GitHub-hosted runners, minimum job permissions, full-SHA action references, no persisted checkout credentials, no dependency cache and no publication/deployment jobs. Dependabot proposes GitHub Actions and Python updates with a seven-day cooldown for version updates; security updates are exempt. See [SECURITY.md](SECURITY.md) for vulnerability reports.

Original material is [MIT licensed](LICENSE). Linked third-party sources retain their own rights.
