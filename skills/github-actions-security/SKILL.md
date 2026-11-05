---
name: github-actions-security
description: "Audit and harden GitHub Actions against malicious pull requests, dependency compromise, credential theft, and unsafe release workflows. Use for an Actions security review or authorized workflow hardening. / Audite e fortaleça o GitHub Actions contra PRs maliciosos, dependências comprometidas, roubo de credenciais e releases inseguros. Use para revisar a segurança do Actions ou aplicar melhorias autorizadas."
license: MIT
metadata:
  author: dayanruben
  version: "1.0.0"
---

# GitHub Actions security / Segurança do GitHub Actions

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

## Fluxo de trabalho

Transforme um pedido de segurança do Actions em achados sustentados por evidências e, quando solicitado, correções focadas. O modelo de ameaça considera uma pessoa atacante externa que controla contribuições ou uma dependência da cadeia de suprimentos. Esta skill não comprova proteção contra uma conta mantenedora comprometida.

1. **Defina o escopo.** Leia as instruções do repositório e confira o estado do Git. Identifique repositório, ref, commit, relação fork/upstream e se o pedido inclui correções ou apenas auditoria. Preserve trabalho não relacionado. Comece pela inspeção estática; não execute código do projeto, instale dependências, dispare workflows privilegiados nem obtenha valores de segredos apenas para auditá-los.
2. **Mapeie os limites de confiança.** Catalogue workflows, workflows reutilizáveis, actions locais e scripts chamados por eles. Para cada job, registre gatilhos, entradas controláveis por atacantes, ref do checkout, runner, permissões efetivas do token, segredos/OIDC, caches, artefatos e efeitos de publicação/deploy. Siga a execução indireta por instaladores, ferramentas de build, actions e consumidores de artefatos. Registre dependências e configurações inacessíveis como desconhecidas.
3. **Revise os controles pertinentes.** Use [o guia de controles](references/controls.pt-BR.md), cobrindo as nove áreas ao revisar um repositório inteiro. Use [fontes e ressalvas de plataforma](references/sources.md) para confirmar sintaxe, disponibilidade de recursos e comportamento de ferramentas sujeitos a mudanças. Separe riscos observáveis de recomendações e controles não aplicáveis.
4. **Aplique correções autorizadas.** Prefira mudanças pequenas que preservem o comportamento esperado de CI e release. Confira commits de actions no histórico do upstream antes de fixá-los. Separe validação em forks de publicação no upstream. Use a autorização existente; a skill não concede autoridade adicional para alterar políticas da organização, credenciais, infraestrutura de runners ou acesso à produção. Não contorne revisões, enfraqueça verificações, reescreva histórico com force-push nem habilite publicação em forks destinados apenas à validação.
5. **Valide sem expor contexto privilegiado.** Execute `actionlint` e `zizmor --strict-collection --persona=pedantic .` quando disponíveis no repositório em escopo, além das verificações existentes pertinentes. Confira cobertura e versões: o zizmor offline não executa auditorias online de procedência. Se verificações online estiverem autorizadas, forneça um token de escopo adequado pelo ambiente, sem imprimi-lo nem colocá-lo nos argumentos de comandos. Inspecione scripts e workflows reutilizáveis manualmente; lint isolado não os cobre. Não instale ferramentas silenciosamente. Confira novamente o diff e o estado do Git e diferencie validação local de resultados remotos de CI para o commit exato.
6. **Relate o resultado.** Identifique escopo/ref/SHA; liste achados por gravidade com `caminho:linha`, entrada da pessoa atacante, caminho de execução, privilégio exposto e mitigação concreta. Inclua mudanças, verificações e cobertura, pontos ainda desconhecidos e configurações que exigem ação de uma pessoa mantenedora. Verificação indisponível significa desconhecida. Uma análise limitada sem achados permite afirmar apenas “nenhum achado no escopo inspecionado”.

**Exemplo de pedido:** “Audite o Actions deste repositório e corrija problemas dentro do escopo dos workflows existentes.”

**Comportamento esperado:** Encontre um workflow privilegiado que executa um script de build da head de um PR; explique como o fork controla o script e quais credenciais do job ficam acessíveis; mova a validação para um job de PR restrito; preserve uma tarefa privilegiada necessária que processe apenas metadados; relate validação e configurações do repositório que não puderam ser consultadas. Não dispare um deploy real para comprovar a correção.
