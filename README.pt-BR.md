# Agent Skills

[Agent Skills](https://agentskills.io/specification) reutilizáveis para fluxos de engenharia de software. Cada skill é autocontida e referencia suas fontes. Revise-a como orientação executável antes do uso.

**Outro idioma:** [English](README.md)

## Catálogo

| Skill | Quando usar |
| --- | --- |
| [github-actions-security](skills/github-actions-security/SKILL.md) | Auditar e fortalecer o GitHub Actions contra ameaças externas em nove áreas de controle, com orientação em inglês e PT-BR. |

## Usar uma skill

Revise a skill e seus arquivos de apoio em um commit específico antes de instalar. Uma skill pode sugerir comandos e ações externas; sua presença não concede credenciais nem autorização adicional.

Clone este repositório e copie o diretório completo `skills/<nome>/` para o local de skills suportado pelo agente. Preserve referências e licença. No Codex, uma instalação de usuário pode usar `~/.agents/skills/<nome>/`; consulte [a documentação atual](https://developers.openai.com/codex/skills) para outros escopos e comportamento de descoberta. Outros agentes têm configuração própria. Armazenar uma skill neste repositório não a ativa automaticamente.

Exemplo de invocação após a configuração:

```text
Use $github-actions-security para auditar os workflows deste repositório.
Relate achados com evidências de arquivo/linha e proponha correções focadas.
```

## Adicionar futuras skills

Adicione `skills/<nome>/SKILL.md` com frontmatter YAML padrão e instruções focadas. Mantenha referências, scripts e assets opcionais dentro desse diretório. Atualize ambos os catálogos e siga [CONTRIBUTING.md](CONTRIBUTING.md) para validação e revisão. Não inclua credenciais, dados operacionais privados, hooks de instalação automática nem execução de código não revisada.

## Validação e segurança do repositório

```sh
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python --require-hashes --no-deps --only-binary=:all: -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/zizmor --offline --strict-collection --persona=pedantic .
```

O validador verifica manifestos, metadados opcionais de interface do Codex e links de arquivos em Markdown inline, incluindo referências autocontidas da skill. Não executa scripts das skills, consulta links externos, avalia afirmações de segurança nem substitui revisão humana. As ferramentas de desenvolvimento com hashes suportam CPython 3.13 em Linux x86_64 e macOS arm64. O zizmor local offline não verifica procedência; a CI usa token de leitura para verificações online em job separado que não executa scripts do repositório.

A CI usa runners hospedados pelo GitHub, permissões mínimas por job, referências de actions com SHA completo, sem credenciais persistidas no checkout, sem cache de dependências e sem jobs de publicação/deploy. O Dependabot propõe atualizações do GitHub Actions e de dependências Python com espera de sete dias para versões; atualizações de segurança são isentas. Consulte [SECURITY.md](SECURITY.md) para relatos de vulnerabilidades.

O material original usa [licença MIT](LICENSE). Fontes de terceiros vinculadas mantêm seus próprios direitos.
