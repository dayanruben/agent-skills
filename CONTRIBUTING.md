# Contributing / Como contribuir

## English

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

Update both README catalogs. Run the validation commands in [README.md](README.md) and `git diff --check`. Dependency updates must refresh the version and compatible wheel hashes together using PyPI's published SHA-256 digests; never remove hash checking to get CI green. Review Dependabot changes for hash coverage and verified upstream action commits. Do not run untrusted updates with privileged credentials.

Open a focused pull request. A maintainer should review instructions, references, scripts, sources, permissions and network behavior before adoption. Packaging validation cannot certify safe behavior. Keep branch protections and required checks intact.

## Português

Crie uma capacidade por diretório em `skills/`, seguindo a [especificação Agent Skills](https://agentskills.io/specification). Comece com `SKILL.md` no formato acima: nome correspondente ao diretório, descrição da tarefa e de quando selecionar a skill e licença aplicável.

Abaixo do frontmatter, escreva propósito, fluxo essencial, saída esperada, tratamento de entradas ausentes e um exemplo realista. Adicione `references/`, `scripts/`, `assets/` e `agents/openai.yaml` apenas quando úteis. Mantenha links relativos dentro da skill e inclua avisos de licença exigidos. Evite credenciais, dados internos, autorização irrestrita de execução, conteúdo genérico e dependências desnecessárias.

Atribua fontes e afirmações sujeitas ao tempo. Prefira documentação primária; não reproduza artigos protegidos por direitos autorais. Teste scripts isoladamente e explique dependências e efeitos colaterais. Auditorias de leitura não devem executar o projeto revisado. Descreva evidências e limites, sem prometer segurança completa.

Atualize ambos os catálogos README. Execute os comandos de validação em [README.pt-BR.md](README.pt-BR.md) e `git diff --check`. Atualizações de dependências devem renovar versão e hashes das wheels compatíveis usando os digests SHA-256 publicados pelo PyPI; nunca remova a checagem de hashes para deixar a CI verde. Revise mudanças do Dependabot quanto à cobertura de hashes e commits de actions verificados no upstream. Não execute atualizações não confiáveis com credenciais privilegiadas.

Abra um pull request focado. Uma pessoa mantenedora deve revisar instruções, referências, scripts, fontes, permissões e comportamento de rede antes da adoção. Validação de empacotamento não certifica comportamento seguro. Preserve proteções de branch e verificações obrigatórias.
