# Fontes, contexto e decisões

Consulta das referências técnicas: 10/11/2026. Conferir documentação e versões novamente no início da implementação. Este pacote descreve um projeto futuro; os critérios de aceite não são resultados de testes já executados.

## Origem da proposta

O usuário pesquisou requisitos de AI Engineer, solicitou os relatórios no Obsidian e escolheu desenvolver um projeto solo/open source para demonstrar competências profissionais. A proposta evoluiu para uma aplicação própria de leitura/gerenciamento de Markdown e manutenção de conhecimento com IA. O usuário quer poder entregar esta documentação a outra IA para implementação posterior.

Decisões preservadas: foco no trabalho de organização e atualização de conhecimento, cuja frequência e importância para os usuários ainda precisam ser verificadas; uso inicial no contexto do Obsidian; independência de um SaaS pré-existente; interface própria; Markdown interoperável; fontes e revisão humana; Python/RAG/agentes/avaliação; escala medida; entrega open source e material de portfólio.

Em 11/11/2026, o usuário solicitou incorporar a explicação da aplicação real e exemplos de uso. O [documento 11](11-aplicacao-real-e-casos-de-uso.md) registra essa discussão, os benefícios como hipóteses, situações de baixo valor e um protocolo de validação. Seus exemplos são cenários ilustrativos definidos na conversa, não estudos de clientes ou resultados observados. Esta atualização não representa nova pesquisa de mercado nem altera a data de consulta das fontes técnicas.

Decisões propostas neste pacote: stack específica, marcos M0–M7, pasta externa somente leitura na v1, um documento por proposta, AWS em host único como primeiro deployment, MCP somente leitura e metas de avaliação. Foram escolhidas para tornar o escopo executável; podem evoluir por ADR e decisão explícita quando alterarem requisitos obrigatórios.

Em 11/11/2026, o usuário escolheu **Traceleaf** como nome do projeto. A identidade deve ser utilizada na aplicação, documentação pública e materiais de portfólio.

## Pesquisa anterior

- [Relatório consolidado](../pesquisa-ai-engineer-2026-11-10.md).
- [Recorte brasileiro](../pesquisa-ai-engineer-brasil-2026-11-10.md).

Amostra qualitativa concentrada em IA aplicada/GenAI. A seleção não mede participação de mercado nem comprova que uma tecnologia é universalmente exigida. Obrigações desta especificação são escolhas de portfólio fundamentadas na amostra, não reprodução integral de qualquer vaga.

## Evidências de vagas

| Fonte oficial | Sinal que contribuiu para a proposta |
|---|---|
| [Arena — AI Engineer](https://job-boards.greenhouse.io/arenaim/jobs/4740889005) | Software em produção, Python, LLMs, recuperação/ferramentas e avaliação |
| [HITSS/Claro — IA Generativa](https://globalhitss.gupy.io/jobs/12758700?jobBoardSource=gupy_public_page) | APIs, agentes, MCP, avaliação, observabilidade e segurança |
| [Capgemini — Python Gen AI Engineer](https://careers.capgemini.com/job/Navi-Mumbai-Python-Gen-AI-Engineer/1442613233/) | Python/SQL, RAG, vetores, cloud e operação de aplicações de IA |
| [Syngenta — AI Engineer Python](https://jobs.smartrecruiters.com/SyngentaGroup/744000143366379-ai-engineer-python) | Engenharia de software, testes, CI/CD, containers e monitoramento |
| [BGBx — AI Engineer](https://job-boards.greenhouse.io/bgbx/jobs/8289189) | Integrações, confiabilidade, fontes e responsabilidade por componentes em produção |

## Documentação técnica primária

- [FastAPI](https://fastapi.tiangolo.com/): contratos HTTP e validação. Conferir integrações e comportamento assíncrono na versão fixada.
- [pgvector](https://github.com/pgvector/pgvector): vetores no PostgreSQL, índices e busca híbrida. Conferir limites da dimensão e comportamento de filtros antes de escolher configuração.
- [LangGraph — interrupções](https://docs.langchain.com/oss/python/langgraph/interrupts): persistência, pausa e retomada para revisão humana.
- [Ragas — faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/): avaliação de suporte da resposta pelo contexto.
- [Langfuse e OpenTelemetry](https://langfuse.com/integrations/native/opentelemetry): integração de traces; verificar SDK/API e evitar captura indevida de conteúdo.
- [Celery — tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html): acknowledgements, idempotência, retries e limites de tarefas.
- [MCP — servidor](https://modelcontextprotocol.io/docs/develop/build-server): SDK, ferramentas e transporte; stdout reservado ao protocolo em stdio.

## ADRs mínimos a escrever durante a implementação

1. Conteúdo canônico em Markdown, snapshots e projeções de busca.
2. Escrita gerenciada e limite de interoperabilidade com editores externos.
3. Chunking, modelo de embeddings, idioma de busca e estratégia de ranking.
4. Escolha de modelo de geração e resultados comparativos.
5. LangGraph, revisão humana e idempotência de efeitos.
6. Avaliação, conjunto final, metas e limitações do juiz LLM.
7. Deploy AWS inicial e fronteiras da escalabilidade demonstrada.
8. Privacidade, retenção, observabilidade e orçamento de uso.

ADRs devem registrar problema, alternativas, decisão, consequências, evidência e condições para revisitar. Uma preferência da IA implementadora, por si só, não comprova vantagem técnica.
