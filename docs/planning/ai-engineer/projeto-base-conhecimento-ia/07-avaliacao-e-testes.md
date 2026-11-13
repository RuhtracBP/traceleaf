# Avaliação de IA, testes e evidências

## Princípio

O portfólio deve demonstrar melhoria medida e limites conhecidos. Testes de software, avaliação de recuperação e avaliação de linguagem são camadas diferentes. Nenhuma delas é substituída por uma demonstração escolhida a dedo.

## Dataset compartilhável

Criar corpus Markdown próprio com documentação de projetos fictícios, pesquisas licenciadas para uso ou conteúdo de autoria do projeto. Incluir PT e EN, versões antigas/atuais, links, tabelas, frontmatter, lacunas e divergências. Registrar licença, origem e hash dos arquivos. Nunca copiar o vault pessoal para o repositório público.

Criar ao menos 120 casos rotulados: perguntas respondíveis e sem resposta, necessidade de várias fontes, atualizações, duplicatas, divergências e conflitos de versão. Separar 80 de desenvolvimento e 40 de avaliação final, estratificados por categoria. Separar também por famílias de documentos/cenários para reduzir vazamento por paráfrases. Corpus gerado para carga não substitui esses casos rotulados.

Formato por caso: `id`, `split`, `category`, `language`, `workspace_fixture`, `source_revisions`, `input`, `expected_evidence`, `expected_action`, `required_claims`, `forbidden_changes`, `rubric`. Revisar manualmente rótulos; casos gerados por LLM não são verdade de referência até conferência humana.

Versionar corpus, splits, prompts, parser, configurações de retrieval e modelos. O conjunto final não deve orientar ajustes cotidianos. Se for usado para corrigir o sistema, declarar isso e reservar novos casos para a próxima avaliação independente.

## Experimentos mínimos

1. Comparar busca textual, vetorial e híbrida sobre os mesmos casos.
2. Comparar duas configurações de chunking no conjunto de desenvolvimento.
3. Comparar dois modelos reais de geração com os mesmos prompts, fontes e condições registradas.
4. Comparar versão inicial e final do fluxo de propostas, contando alterações indevidas e fontes corretas.
5. Registrar trade-offs: uma melhora de qualidade com mais latência/custo não é automaticamente a melhor escolha.

Usar Ragas para métricas semânticas adequadas à versão escolhida, incluindo faithfulness quando aplicável. Avaliação por modelo é um sinal auxiliar: registrar juiz, prompt e versão e auditar manualmente pelo menos 20 resultados finais, distribuídos por categoria. Faithfulness mede suporte no contexto, não verdade externa. [Referência](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/).

## Métricas e metas iniciais

As metas abaixo são propostas de engenharia para a v1, não resultados obtidos nem padrões universais de contratação. Fixar a versão das metas antes da avaliação final. Publicar numerador, denominador, categorias, erros e incerteza; não divulgar apenas uma média agregada.

| Métrica | Definição | Meta inicial |
|---|---|---|
| Recall@5 de evidência | Média por caso da fração de trechos/documentos de referência recuperados entre os cinco primeiros | ≥ 0,85 nos casos respondíveis |
| Precisão das citações | Citações que sustentam a afirmação associada / citações avaliadas, por revisão humana | ≥ 0,95 na amostra auditada |
| Afirmações sem suporte | Afirmações factuais sem evidência suficiente / afirmações factuais avaliadas | ≤ 0,05 na amostra auditada |
| Abstenção correta | Casos sem resposta em que o sistema indica insuficiência / casos sem resposta | ≥ 0,90 |
| Sucesso de proposta | Casos em que ação, preservação e fontes satisfazem a rubrica / casos de proposta | ≥ 0,80 |
| Validade estrutural | Saídas válidas após no máximo dois reparos / gerações avaliadas | ≥ 0,98; casos inválidos falham explicitamente |
| Integridade e isolamento | Casos técnicos de segurança/concorrência aprovados | 100% da suíte crítica |
| Custo | Tokens e estimativa monetária por resposta/proposta; custos de ingestão e juiz separados | Publicar distribuição, sem teto monetário inventado |
| Latência | p50/p95 por busca, geração e aplicação; sucesso/falha separados | Medir e identificar gargalos |

Quando a meta não for atingida, registrar falha, exemplos e plano; não alterar retrospectivamente o limiar para “passar”. Bloqueios críticos de integridade impedem release. Metas semânticas não atingidas mantêm o marco de qualidade pendente ou exigem decisão explícita de release experimental com limitações.

## Testes de software

- Unitários focados: parser/preservação, resolução de paths, hashing, fusão de rankings, schemas, estados e permissões.
- Integração com PostgreSQL/pgvector real: isolamento, migrations, troca de índice, consultas e transações.
- Integração com Redis/Celery real: redelivery, lease vencido, retries, cancelamento e outbox.
- Integração com filesystem temporário: journal, falhas entre etapas, rename, restore e conflitos.
- Playwright: importar → perguntar com fonte → propor → editar/revisar → aprovar/aplicar → restaurar.
- Adversariais: prompt injection, path traversal, XSS, acesso cruzado entre workspaces e orçamento excedido.
- Contratos: HTTP e MCP compartilham autorização, retornam evidências equivalentes e respeitam limites.

CI sem credenciais usa doubles determinísticos de modelos para testar controle de fluxo. Avaliações semânticas usam modelos reais em execução manual ou agendada autorizada. Relatórios devem rotular claramente `mock`, `cached` e `live`; resultado cached não é uma nova medição de latência/custo.

## Desempenho e recuperação

Usar corpora de 100/1.000/10.000 documentos, medir quantidade e tamanho de chunks e repetir cenários de concorrência 1/5/10. Separar geração de embeddings da consulta ao banco, e latência do provedor da aplicação. Publicar consumo de CPU/memória e tamanho de índice.

Meta orientadora: p95 da recuperação no banco ≤ 2 s com 10 consultas simultâneas e 10.000 documentos em ambiente de referência explicitado. Não inclui chamada de embedding, geração nem rede do usuário. Reportar resultado mesmo quando falhar; o relatório deve apontar a capacidade observada, não garantir esse alvo em qualquer hardware.

Alterar um arquivo e demonstrar que apenas seus trechos afetados exigem novo processamento. Derrubar um worker e simular falhas antes/depois da escrita para validar recuperação. O teste de escala deve incluir resultados corretos, não apenas taxa de requests.

## Artefatos

Entregar `evals/dataset.jsonl`, splits, runner, configurações, resultados estruturados e `docs/evaluation-report.md`. Relatório: commit, data, ambiente, versões, modelos, custos com data de referência, amostra, comparações, auditoria humana e casos de falha. Disponibilizar um comando para reproduzir cada experimento.

O aprendizado do usuário faz parte do objetivo: incluir um estudo de caso explicando pelo menos três decisões com dados, por exemplo chunking, busca híbrida e escolha do modelo. Não atribuir ganhos ao projeto sem baseline comparável.
