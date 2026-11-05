# Controles contra ameaças externas

Use as seções correspondentes ao workflow. Em auditorias do repositório inteiro, marque cada área como revisada, não aplicável ou desconhecida, com evidências. Consulte [as fontes mantidas](sources.md) antes de depender de recursos em prévia ou comportamentos específicos de versões.

## 1. Dependências de actions e workflows

- Inspecione cada `uses` remoto, incluindo workflows reutilizáveis e actions compostas aninhadas. Prefira SHAs completos verificados quando lockfiles não estiverem disponíveis ou não cobrirem uma referência. Fixe imagens por digest. Um SHA direto não congela `uses` aninhados, imagens-base Docker, downloads de pacotes nem a CLI baixada por um wrapper.
- Quando suportados, avalie lockfiles de dependências de workflows do GitHub com verificação da identidade do upstream e cobertura transitiva. Comece pelos repositórios de workflows compartilhados. Gere e verifique com ferramentas oficiais; revise commits e identidades alterados. Não edite lockfiles manualmente, presuma cobertura de chamadas a workflows reutilizáveis ou contêineres nem imponha uso antes de cobrir todos os workflows selecionados.
- Resolva a versão no upstream real e confirme que o commit é alcançável pelo seu histórico. Encontrar um commit pela API na URL do upstream é insuficiente: redes de forks podem expor ali commits existentes apenas em forks. Um commit malicioso imutável continua malicioso. Nunca invente um SHA nem faça commit de marcadores de exemplo da documentação.
- Mantenha comentários com a versão revisada e um processo de atualização. Confira a cobertura de avisos de segurança para o formato escolhido; PRs de versão não garantem alertas de vulnerabilidade. Não substitua mecanicamente um lockfile válido e imposto por pins inline.

## 2. Tokens, segredos e publicação

- Prefira `permissions: {}` no workflow e concessões mínimas explícitas por job. Confira permissões efetivas, herança em workflows reutilizáveis, tokens PAT/App e `secrets: inherit`; reduzir `GITHUB_TOKEN` não restringe credenciais independentes. Use `persist-credentials: false` quando operações Git autenticadas posteriores não forem necessárias.
- Conceda `id-token: write` apenas ao job que precisa de OIDC. Qualquer etapa desse job pode solicitar um token: uma variável restrita à publicação não isola etapas hostis de build/instalação. Restrinja a confiança do provedor ao repositório, workflow/ref ou ambiente protegido pretendidos e à audiência.
- Separe build de publicação. Mantenha credenciais de publicação fora do build; use um job mínimo que consuma saídas verificadas sem hooks do projeto nem código recém-baixado não revisado. Confira proteções de ambiente e quem pode aprovar. Sem acesso às configurações, não afirme imposição.
- Em forks de validação de compatibilidade, preserve a validação e impeça publicação de pacotes/releases, envio de contêineres e deploy de documentação. Preserve releases do upstream no contexto confiável previsto.

## 3. Gatilhos privilegiados e artefatos

- Prefira `pull_request` para contribuições não confiáveis, com permissões restritas e sem segredos. Confira configurações reais de forks/repositórios privados em vez de presumir padrões. Inspecione `pull_request_target`, `workflow_run`, comentários, dispatches e entradas reutilizáveis em busca de execução indireta não confiável.
- Em contextos privilegiados, não faça checkout nem execute a head de PR, seus scripts, dependências, actions locais ou executáveis de artefatos. Checkout da base só ajuda se as etapas seguintes também evitarem execução controlada por atacantes. Não desative proteções de checkout de PRs inseguros como correção.
- Um workflow privilegiado separado não é automaticamente seguro. Vincule downloads ao ID da execução disparadora; confira repositório, identidade do workflow, evento, ref/SHA da head, conclusão e identidade do artefato para a operação prevista. Sucesso isolado é insuficiente. Valide nomes, limites de tamanho e esquema; rejeite extração fora do destino e links inseguros. Nunca use source, eval nem execute relatórios não confiáveis.
- Publique apenas saídas do build/ref confiável previsto; integridade do download não torna um artefato de fork publicável. Minimize uploads e exclua credenciais, dados internos do workspace e arquivos com segredos.

## 4. Injeção de expressões e comandos

Rastreie textos de PRs/issues, nomes de branches, mensagens de commit, entradas de workflows e dados baixados até `run`, entradas de scripts, avaliação de shell e arquivos de comandos. A confiança depende de quem controla o valor, não de um prefixo `github.event`.

Passe dados por uma variável de ambiente e use aspas ao acessá-la:

```yaml
- name: Read the title as data
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: printf '%s\n' "$PR_TITLE"
```

Não substitua a expressão diretamente no código de shell ou de `actions/github-script`. Em JavaScript, leia `context.payload` ou `process.env`. Evite `eval`, entradas passadas a `bash -c` e construção insegura de argumentos. Valide dados escritos em `GITHUB_ENV`, `GITHUB_OUTPUT` e `GITHUB_PATH`; um valor em `env:` não torna seguras escritas posteriores em arquivos de comandos. Use formatos fixos e trate dados multilinha corretamente. Não execute o payload de uma pessoa atacante para demonstrar injeção.

## 5. Limites de cache

- Mapeie eventos/refs com escrita e consumidores privilegiados, incluindo caches automáticos de setup. O escopo é propriedade do serviço; prefixos e hashes de lockfiles não são controle de acesso. Caches comuns de merge-ref de PRs não podem ser restaurados pela base; PRs de forks podem ler caches elegíveis da base. Nunca armazene segredos em cache.
- Confira padrões atuais e substituições explícitas de `cache-mode`. Quando suportado, limite jobs não confiáveis a `read` ou `none` e use `none` para releases limpos. Substituições com escrita em baixa confiança podem reabrir limites protegidos. Confira a aplicação a workflows reutilizáveis.
- Sem controles no serviço, remova produtores/consumidores inseguros e desative caches pertinentes de setup. Etapas só de restauração expressam intenção, mas não restringem código malicioso com token independente de cache. Evite caches executáveis de procedência incerta na publicação.

## 6. Runners

- Prefira runners hospedados pelo GitHub para contribuições externas. Aprovação de primeira contribuição, labels e verificações de nomes de usuário não estabelecem isolamento durável.
- Se hardware próprio for necessário, inspecione restrições de grupos/workflows, agendamento não confiável, workspaces persistentes, credenciais, jobs vizinhos, endpoints de metadados e alcance de rede. Use hosts efêmeros isolados com descarte/recriação após cada job. Remover o registro ou apagar o workspace não comprova limpeza do host.
- Separe jobs públicos não confiáveis de cargas privadas e redes de produção. Marque controles de infraestrutura não verificáveis como desconhecidos. Não reconfigure runners ativos como efeito colateral da auditoria de YAML.

## 7. Entrada de dependências

- Use instalações determinísticas com lockfiles versionados e verificação quando suportada. Inspecione substituições de registries, dependências Git/URL/caminho, hooks e plugins de build. Para Gradle, examine locking, metadados de verificação e integridade do wrapper em vez de aplicar comandos npm.
- Mantenha credenciais fora da instalação. Desative scripts de ciclo de vida quando compatível e revise exceções; preserve builds nativos necessários com uma lista restrita em vez de quebrar a CI silenciosamente.
- Avalie controles de idade de release na resolução e nos bots. Instalações congeladas consomem um lockfile e não reaplicam a espera da resolução. Confira suporte e unidades do gerenciador; não atrase correções urgentes com um período universal arbitrário.

## 8. Scripts e uploaders baixados

- Encontre instaladores enviados diretamente ao shell, executáveis baixados e ferramentas obtidas dentro de actions. Fixe versões dos payloads; confira integridade com digest revisado e versionado ou assinaturas autenticadas por chave/pessoa signatária de confiança independente. Checksums do mesmo local mutável não autenticam independentemente uma distribuição comprometida.
- Inspecione padrões de wrappers e entradas que desativam verificações: o SHA de uma action ainda pode baixar uma CLI `latest`. Preserve verificações e mantenha downloads fora de contextos privilegiados de build quando possível. HTTPS e URLs que parecem versionadas não comprovam integridade.

## 9. Acesso à rede e risco residual

- Catalogue destinos necessários antes de propor restrições de saída. Comece por auditoria observável, depois uma lista restrita mantida e alertas de bloqueio. Confira se jobs não confiáveis não podem ampliar a imposição; considere metadados de nuvem, serviços internos e redes de produção. Não instale um agente de rede silenciosamente nem presuma que um recurso planejado existe.
- Serviços permitidos e logs públicos continuam sendo canais de exfiltração. Filtragem complementa privilégio mínimo; não torna segura a execução de código hostil com segredos.
- Declare riscos residuais: contas mantenedoras comprometidas, dependências desconhecidas, configurações inacessíveis e comportamento em execução excedem o que a revisão estática comprova. Não apresente estes controles como garantia completa de segurança.
