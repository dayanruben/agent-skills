# Repository instructions

- Store reusable Agent Skills, documentation and validation tooling here. Keep product code and private operational data out.
- Put each skill in `skills/<name>/` with matching YAML `name` and a useful trigger description. Follow the Agent Skills specification. Keep references, optional scripts/assets and required license notices inside the skill directory so it remains portable.
- Keep instructions focused; move substantial conditional details into linked references. Preserve task scope and existing authorization. Skills must not grant themselves credentials, bypass safeguards or silently install or execute dependencies.
- Cite sources and write independent instructions rather than copying articles. Verify changing technical claims in primary documentation. Preserve third-party rights and attribution.
- Keep English and PT-BR catalogs equivalent. Update existing translated instructions and references together.
- Run `python scripts/validate_skills.py`, `python -m unittest discover -s tests -v`, and `git diff --check` in the documented environment. Inspect Git status. Review workflow changes with actionlint and security analysis when available; report missing coverage honestly.
- Preserve unrelated edits. Use pull requests after initial creation and respect required checks/reviews. Do not add publication/deployment automation without an explicit request.
