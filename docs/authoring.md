# Authoring portable skills

This collection uses the [Agent Skills specification](https://agentskills.io/specification) and the [skills.sh discovery layout](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md). Keep one capability per `skills/<name>/` directory, with a matching manifest name and a description that states the task and its selection criteria. Use English throughout.

## Patterns from leading skills

Reviewed against the [skills.sh leaderboard](https://www.skills.sh/) on November 5, 2026. Rankings change; popularity is a discovery signal, not evidence of security. These are authoring references, not runtime dependencies or copied instructions.

| Reference | Pattern adopted here |
| --- | --- |
| [Vercel's find-skills](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md) | Make the capability and intended requests easy to identify; include an explicit installation and invocation example. |
| [Vercel's React best practices](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) | Keep the entrypoint focused, organize guidance by decision area, and link detailed explanations and examples for selective reading. |
| [The skills CLI authoring guide](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md) | Use standard YAML metadata and a discoverable directory layout without requiring a custom installer. |

Adapt these structures to the task. Do not import unrelated domain rules, mandatory tools, popularity thresholds, or cross-skill dependencies.

## Write and review

Put scope, important trust boundaries, workflow and output expectations in `SKILL.md`. Move substantial conditional detail into linked references. Include a realistic request and observable expected behavior; add scripts only when deterministic execution helps. Keep references and license notices inside the skill so copying or installing it preserves context.

For security skills, distinguish static evidence, runtime evidence and unavailable settings. An audit does not authorize execution of the project under review. Fixes must retain user intent, repository safeguards and existing authorization boundaries.

Review realistic prompts before sharing: a request that should activate the skill, a similar task that should not, an incomplete-input case, and an adversarial trust-boundary case. For `github-actions-security`, compare a PR-head build in a privileged job with a metadata-only labeler; also review an artifact consumer and an injection-prone script. Check whether the guidance leads to concrete evidence and preserves legitimate validation. Packaging checks alone do not evaluate the model's decisions.

## Validate discovery and updates

Run the README checks, including the pinned official CLI's `skills add . --list`. Listing must expose the public catalog without installing anything. A repository under the standard `skills/` layout needs no custom discovery paths. Do not set `metadata.internal` on published catalog entries.

For an installation smoke test, use a disposable project, select an agent explicitly, and redirect CLI state with `XDG_STATE_HOME`; disable telemetry during tests. Verify that references and license files arrive, and avoid modifying real global skill installations. Review current [CLI options](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) before scripting installation or updates.

The public Git repository is the distribution source. The skills.sh directory tracks user installations as described in [its FAQ](https://www.skills.sh/docs/faq); a successful discovery test does not prove a leaderboard listing or endorsement. Keep automation free of publishing credentials and sign every commit.
