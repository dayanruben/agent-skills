# Sources and maintenance

## Attribution

Inspired by Karlo Zanki's [Hardening GitHub Actions Against Outside Threats](https://socket.dev/blog/hardening-github-actions-against-outside-threats), Socket, published November 3, 2026; consulted November 5, 2026. The nine control areas follow that article's outside-attacker model. These instructions and examples are independently written; the article is linked, not redistributed or relicensed. This skill is not affiliated with Socket or GitHub.

## Primary references

| Topic | Source |
| --- | --- |
| Permissions, injection, third-party actions and runners | [GitHub: Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) |
| Triggers and privileged contexts | [GitHub: Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) |
| Lockfile generation and coverage | [GitHub: Locking action dependencies](https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies) |
| Lockfile rollout and enforcement | [GitHub: Enforcing lockfiles](https://docs.github.com/en/actions/how-tos/administer/enforce-workflow-lockfiles) |
| Cache scope and service-side permissions | [GitHub: Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) |
| Short-lived cloud credentials | [GitHub: OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect) |
| Linter scope and usage | [actionlint](https://github.com/rhysd/actionlint) |
| Static and online security audits | [zizmor: Usage](https://docs.zizmor.sh/usage/), [Audit rules](https://docs.zizmor.sh/audits/) |

## Recheck before applying

- **Platform support:** GitHub.com, Enterprise Cloud and Enterprise Server differ. Lockfile availability and enforcement scope can change. Verify current coverage, plan/version eligibility, policy interactions and reusable-workflow requirements before adoption. Full verified SHAs remain the fallback for uncovered references.
- **Defaults and syntax:** Cache modes, fork approvals, token defaults and checkout protections change. Verify current documentation and actual settings; do not treat historical exploit conditions, rollout dates or example versions as present facts.
- **Tool coverage:** Record versions, selected inputs, parse errors and skipped checks. Use strict zizmor collection. Offline results omit online provenance checks; actionlint does not establish security. Neither tool verifies actual runner, cloud or organization policy enforcement.
- **Evidence:** Link findings to inspected code and, when available, exact-commit runs. Avoid incident counts, detection-rate estimates or product recommendations unnecessary to the decision.
