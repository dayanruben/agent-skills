# Sources and maintenance / Fontes e manutenção

## Attribution / Atribuição

Inspired by Karlo Zanki's [Hardening GitHub Actions Against Outside Threats](https://socket.dev/blog/hardening-github-actions-against-outside-threats), Socket, published November 3, 2026; consulted November 5, 2026. The nine control areas follow that article's outside-attacker model. These instructions and examples are independently written; the article is linked, not redistributed or relicensed. This skill is not affiliated with Socket or GitHub.

Inspirada em [Hardening GitHub Actions Against Outside Threats](https://socket.dev/blog/hardening-github-actions-against-outside-threats), de Karlo Zanki, Socket, publicado em 3 de novembro de 2026; consultado em 5 de novembro de 2026. As nove áreas seguem o modelo de ameaça externa do artigo. As instruções e exemplos foram escritos de forma independente; o artigo é referenciado, sem redistribuição ou alteração de sua licença. Esta skill não tem afiliação com Socket ou GitHub.

## Primary references / Referências primárias

| Topic / Tema | Source / Fonte |
| --- | --- |
| Permissions, injection, third-party actions and runners / Permissões, injeção, actions de terceiros e runners | [GitHub: Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) |
| Triggers and privileged contexts / Gatilhos e contextos privilegiados | [GitHub: Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) |
| Lockfile generation and coverage / Geração e cobertura de lockfiles | [GitHub: Locking action dependencies](https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies) |
| Lockfile rollout and enforcement / Adoção e imposição de lockfiles | [GitHub: Enforcing lockfiles](https://docs.github.com/en/actions/how-tos/administer/enforce-workflow-lockfiles) |
| Cache scope and service-side permissions / Escopo de cache e permissões no serviço | [GitHub: Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) |
| Short-lived cloud credentials / Credenciais de nuvem de curta duração | [GitHub: OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect) |
| Linter scope and usage / Escopo e uso do linter | [actionlint](https://github.com/rhysd/actionlint) |
| Static and online security audits / Auditorias estáticas e online de segurança | [zizmor: Usage](https://docs.zizmor.sh/usage/), [Audit rules](https://docs.zizmor.sh/audits/) |

## Recheck before applying / Confira antes de aplicar

- **Platform support:** GitHub.com, Enterprise Cloud and Enterprise Server differ. Lockfile availability and enforcement scope can change. Verify current coverage, plan/version eligibility, policy interactions and reusable-workflow requirements before adoption. Full verified SHAs remain the fallback for uncovered references. / **Suporte:** GitHub.com, Enterprise Cloud e Enterprise Server diferem. Disponibilidade de lockfiles e escopo de imposição podem mudar. Confira cobertura, elegibilidade por plano/versão, interação de políticas e requisitos de workflows reutilizáveis. SHAs completos verificados continuam sendo a alternativa para referências não cobertas.
- **Defaults and syntax:** Cache modes, fork approvals, token defaults and checkout protections change. Verify current documentation and actual settings; do not treat historical exploit conditions, rollout dates or example versions as present facts. / **Padrões e sintaxe:** Modos de cache, aprovações de forks, permissões padrão e proteções de checkout mudam. Confira documentação atual e configurações reais; não trate condições históricas de exploração, datas de adoção nem versões de exemplo como fatos atuais.
- **Tool coverage:** Record versions, selected inputs, parse errors and skipped checks. Use strict zizmor collection. Offline results omit online provenance checks; actionlint does not establish security. Neither tool verifies actual runner, cloud or organization policy enforcement. / **Cobertura:** Registre versões, entradas, erros de parsing e verificações omitidas. Use coleta estrita no zizmor. Resultados offline não incluem verificações online de procedência; actionlint não comprova segurança. Nenhuma ferramenta verifica imposição real de políticas de runners, nuvem ou organização.
- **Evidence:** Link findings to inspected code and, when available, exact-commit runs. Avoid incident counts, detection-rate estimates or product recommendations unnecessary to the decision. / **Evidências:** Vincule achados ao código e, quando disponíveis, a execuções do commit exato. Evite números de incidentes, estimativas de detecção ou recomendações de produtos desnecessários à decisão.
