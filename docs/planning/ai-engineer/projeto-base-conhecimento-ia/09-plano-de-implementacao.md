# Plano de implementação e conclusão

## Como executar

Os marcos abaixo são dependências, não estimativas de prazo. Uma IA futura deve criar tarefas pequenas dentro de cada marco e manter `docs/implementation-status.md` atualizado. Cada item marcado concluído deve apontar para código, comando/teste e resultado. Preservar a distinção entre implementado, validado com doubles, validado com modelo real e validado em cloud.

## M0 — Fundação e decisões

Ler [11](11-aplicacao-real-e-casos-de-uso.md), [01](01-produto-e-requisitos.md), [02](02-stack-e-empregabilidade.md), [03](03-arquitetura.md) e [06](06-integridade-e-seguranca.md). Selecionar o caso de uso inicial e registrar público, tarefa atual, hipótese de benefício e exemplos disponíveis em `docs/product-validation.md`. Criar monorepo, dependências fixadas, Compose, CI básico e configuração. Registrar ADRs de storage, modelo/provedor, stack, versões e limites iniciais de custo/execução.

**Concluído quando:** clone limpo sobe web/API/banco/Redis, checks básicos passam, migrations funcionam e README reproduz a instalação. Nenhuma dependência obrigatória é silenciosamente removida. Sem credencial de IA, o sistema informa a capacidade indisponível.

O caso de uso inicial e o plano de comparação com o processo habitual também devem estar registrados. Falta de exemplos reais não deve ser mascarada por dados sintéticos: registrar a validação de produto como pendente e continuar a implementação com fixtures.

## M1 — Produto Markdown utilizável

Implementar workspaces, identidade/autorização, importação, biblioteca, leitor/editor, frontmatter, links, criação, movimento, arquivo, histórico e exportação. Pasta externa é leitura; workspace gerenciado permite escrita versionada. Criar corpus de demonstração e primeiros casos de teste.

**Concluído quando:** RF01–RF05 e RF12/RF14 passam em testes de integração/e2e, arquivos exportados abrem como Markdown comum e duas sessões não acessam workspaces alheios. Alterações concorrentes geram conflito em vez de overwrite silencioso.

## M2 — Busca e respostas fundamentadas

Implementar parser/chunking, embeddings, índice incremental, busca textual/vetorial/híbrida, filtros e perguntas com fontes. Introduzir outbox, jobs e workers. Criar dataset de desenvolvimento, baselines e orçamento de execução. Ler [05](05-rag-e-agentes.md) e [07](07-avaliacao-e-testes.md).

**Concluído quando:** busca e resposta reais funcionam no corpus; fonte abre no snapshot correto; pergunta sem suporte gera insuficiência; modificar um documento não reprocessa toda a base. Publicar primeiro relatório de recuperação e uma execução de modelo real.

## M3 — Propostas e revisão humana

Implementar grafo LangGraph persistente, ferramentas, schemas, propostas create/update/no_change, diff, edição/rejeição/aprovação e aplicação com journal. Executar UC01 e UC02 de [11](11-aplicacao-real-e-casos-de-uso.md) e os cenários de divergência, duplicata, fonte alterada e restauração. Implementar recuperação após interrupção/reinício.

**Concluído quando:** os seis cenários de [01](01-produto-e-requisitos.md) são demonstráveis e os casos críticos de [06](06-integridade-e-seguranca.md) passam. Uma execução pausada retoma após reinício e não aplica sem aprovação válida. Neste ponto existe um MVP funcional; o portfólio ainda não está completo.

## M4 — Operação confiável

Implementar traces OpenTelemetry/Langfuse, custo, métricas, limites, cancelamento, retries, leases, reconciliação e runbooks. Exercitar falhas de banco, worker, provedor e filesystem. Usar [08](08-operacao-e-implantacao.md).

**Concluído quando:** um run é rastreável de ponta a ponta, reentrega não duplica mudança, falha de telemetria não bloqueia edição e recuperação preserva arquivos. Publicar trace sanitizado e relatório dos testes de falha.

## M5 — Qualidade e escala medidas

Finalizar dataset/splits, comparação de retrieval/chunking/modelos, Ragas, auditoria humana e benchmark de carga. Registrar achados e ADRs com evidências. Manter resultado desfavorável no relatório quando ocorrer.

Quando houver exemplos e participantes disponíveis, executar a comparação de utilidade descrita em [11](11-aplicacao-real-e-casos-de-uso.md). Registrar tempo total, correções, documentos afetados encontrados e motivos de rejeição em `docs/product-validation.md`. Sem teste real, deixar explícito que desempenho técnico não comprova utilidade nem demanda.

**Concluído quando:** avaliações são reproduzíveis, metas e falhas de [07](07-avaliacao-e-testes.md) estão explicitadas, integridade passa integralmente e capacidade observada está documentada. Metas semânticas não atingidas seguem o procedimento de release experimental/pendência, sem resultados inventados.

## M6 — Distribuição, CI e cloud

Finalizar instalação, pipeline de release, Docker, backups e restore. Criar Terraform AWS e demo com dados compartilháveis. Executar deployment e smoke test quando credenciais/orçamento forem autorizados; preparar passo a passo e validação de configuração enquanto isso.

**Concluído quando:** terceiro consegue instalar com README, CI passa, restauração foi testada e ambiente AWS tem evidência real. Se a implantação não foi autorizada, marcar M6 parcialmente validado e listar precisamente a pendência externa; não bloquear preparação de M7.

## M7 — Open source, MCP e portfólio

Implementar ferramentas MCP somente leitura, testar cliente e documentar configuração. Preparar licença open source para código próprio (Apache-2.0 como padrão proposto), conferir licenças das dependências e do corpus, e escrever CONTRIBUTING/SECURITY. Publicar README principal em inglês e guia pt-BR.

Preparar vídeo de 3–5 minutos, estudo de caso, diagramas, relatório de avaliação e `docs/skills-evidence.md`. Mostrar problema, fluxo real, uma falha tratada e um trade-off medido. Código público, publicação de release e gravação podem exigir conta/ação do usuário; deixar artefatos prontos e registrar pendências.

**Concluído quando:** MCP executa buscas autorizadas reais, licença e dados são revisados, documentação permite reprodução e todas as afirmações de capacidade apontam para evidências. Nenhuma credencial ou nota privada é publicada.

## Matriz final de rastreabilidade

Criar `docs/acceptance-matrix.md` com RF01–RF16, todos os eixos obrigatórios de [02](02-stack-e-empregabilidade.md), testes críticos de [06](06-integridade-e-seguranca.md) e artefatos de [07](07-avaliacao-e-testes.md)/[08](08-operacao-e-implantacao.md). Cada linha inclui status, evidência, limitação e marco. A entrega só pode ser declarada completa com a matriz preenchida e pendências externas claramente separadas.

## Pacote final esperado

- Código executável com UI, API, workers, migrations e MCP.
- Instalação local reproduzível e exemplos sem credenciais pessoais.
- Corpus licenciado, casos rotulados e avaliações com resultados reais.
- Tests/CI e relatório de recuperação/integridade.
- Infraestrutura AWS, backup/restore e registro de implantação ou pendência externa.
- README inglês, guia pt-BR, ADRs, arquitetura, API e runbooks.
- Estudo de caso com baselines, decisões, falhas e limitações, incluindo `docs/product-validation.md` com evidências de utilidade ou validações pendentes.
- Demo e roteiro de vídeo que o usuário possa apresentar em entrevistas.

## O que o usuário deve conseguir explicar

Por que o chunking escolhido funciona; como a busca foi avaliada; por que o modelo foi selecionado; como se verificam fontes; como o agente usa ferramentas e pausa; como se evita duplicar efeitos; como se protege isolamento; como se recupera uma escrita parcial; quanto uma operação custa; qual carga foi testada; o que seria necessário para escalar além dela.

Não alegar garantia de contratação. O resultado esperado é evidência técnica defensável e um produto utilizável, com autoria e contribuição da IA descritas com honestidade.
