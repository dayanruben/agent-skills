# Repository instructions

- Store reusable Agent Skills, documentation and validation tooling here. Keep product code and private operational data out.
- Put each skill in `skills/<name>/` with matching YAML `name` and a useful trigger description. Follow the Agent Skills specification. Keep references, optional scripts/assets and required license notices inside the skill directory so it remains portable.
- Keep instructions focused; move substantial conditional details into linked references. Preserve task scope and existing authorization. Skills must not grant themselves credentials, bypass safeguards or silently install or execute dependencies.
- Cite sources and write independent instructions rather than copying articles. Verify changing technical claims in primary documentation. Preserve third-party rights and attribution.
- Use English for all repository documentation, skill instructions, metadata and examples. Update the README catalog when skills change. Keep packaging compatible with the skills.sh CLI.
- Follow [the authoring guide](docs/authoring.md) for source attribution, concise triggers, progressive references and behavioral review. Check discovery with `DISABLE_TELEMETRY=1 npm run check:skills` after `npm ci --ignore-scripts --no-audit --no-fund`.
- Run `python scripts/validate_skills.py`, `python -m unittest discover -s tests -v`, and `git diff --check` in the documented environment. Inspect Git status. Review workflow changes with actionlint and security analysis when available; report missing coverage honestly.
- Preserve unrelated edits. Use signed commits and pull requests, and respect required checks/reviews. Do not add publication/deployment automation without an explicit request.
