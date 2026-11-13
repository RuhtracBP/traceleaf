# Stack obrigatória e relação com vagas

## Intenção

O projeto DEVE demonstrar tecnologias e competências recorrentes na pesquisa de vagas de AI Engineer. A amostra é qualitativa: não prova que uma biblioteca específica é a mais pedida do mercado. Python, LLMs, RAG, APIs, agentes, avaliação, cloud e operação são os eixos observados. Bibliotecas de suporte abaixo são escolhas de implementação para materializar esses eixos.

Vagas como [Arena](https://job-boards.greenhouse.io/arenaim/jobs/4740889005), [HITSS](https://globalhitss.gupy.io/jobs/12758700?jobBoardSource=gupy_public_page) e [Capgemini](https://careers.capgemini.com/job/Navi-Mumbai-Python-Gen-AI-Engineer/1442613233/) sustentam essa combinação. Frameworks específicos podem ser requisitos ou diferenciais conforme o anúncio. A [Syngenta](https://jobs.smartrecruiters.com/SyngentaGroup/744000143366379-ai-engineer-python) reforça qualidade de software, testes, entrega e operação.

## Tecnologias obrigatórias na entrega completa

| Eixo | Escolha | Uso real e evidência exigida | Marco |
|---|---|---|---|
| Backend | Python, FastAPI, Pydantic | API tipada, validação de schemas, I/O assíncrono, erros e testes de integração | M0–M1 |
| Dados | PostgreSQL, SQLAlchemy, Alembic | Modelo relacional, migrations, transações, integridade e SQL inspecionável | M1 |
| Busca | pgvector e full-text do PostgreSQL | Busca vetorial e textual combinadas; comparação com baselines | M2 |
| LLM | SDK oficial de um provedor, atrás de uma interface interna | Geração estruturada, tool calling, timeouts, uso de tokens e limites reais | M2–M3 |
| Embeddings | Modelo de embeddings configurável | Indexação real, identificação do modelo/dimensão e reindexação controlada | M2 |
| Agentes | LangGraph | Grafo com estado persistido, ferramentas, interrupção para revisão e retomada | M3 |
| Processamento | Celery e Redis | Jobs duráveis no PostgreSQL, execução em workers, retry e idempotência | M2–M4 |
| Frontend | TypeScript, React, Vite, editor CodeMirror | Biblioteca, Markdown, diff e acompanhamento de jobs conectados à API | M1–M3 |
| Avaliação | pytest e Ragas | Benchmarks determinísticos e avaliação de fundamentação; relatório real | M2–M5 |
| Observabilidade | OpenTelemetry e Langfuse | Correlação API/worker/modelo; traces de IA e medição de custo/latência | M4 |
| Qualidade | Ruff, verificação de tipos Python, Vitest, Playwright | Checks de backend/frontend e testes dos fluxos críticos | Todos |
| Entrega | Docker, Docker Compose, GitHub Actions | Instalação reproduzível, CI, build e imagens identificáveis | M0–M6 |
| Cloud/IaC | AWS e Terraform | Ambiente de referência, validação de configuração e demonstração de implantação autorizada | M6 |
| Interoperabilidade de IA | MCP, SDK oficial | Servidor local somente leitura para pesquisar e consultar evidências | M7 |

MCP é uma capacidade complementar encontrada na pesquisa, incluída deliberadamente no portfólio. Não substitui REST nem é requisito universal. Celery, Redis, CodeMirror e Vite são decisões técnicas deste projeto; não atribuir a eles ranking de demanda.

## Escolhas específicas

- Implementar primeiro um provedor real de geração e embeddings; registrar a escolha em ADR com custo observado, qualidade e capacidade de saída estruturada. Selecionar modelos na data da implementação e registrar identificadores; não usar nomes inventados ou assumir que `latest` é reproduzível.
- Uma interface `ModelGateway` deve oferecer geração estruturada, chamadas de ferramentas e embeddings, sem obrigar todos os modelos a suportar tudo. Validar capacidades na configuração.
- Um segundo modelo de geração real deve ser comparado na avaliação final. Pode ser do mesmo provedor. Um adaptador local via Ollama é extensão, não requisito da v1.
- Usar LangGraph para a orquestração. Utilitários de LangChain podem ser usados quando necessários; instalar LangChain, LlamaIndex e outros frameworks simultaneamente não é objetivo.
- SQLAlchemy/Alembic são a escolha padrão de persistência; usar SQL direto quando necessário para full-text, vetores, locks e análise de plano.
- Utilizar `uv` e `pnpm` como ferramentas de dependências, fixando versões. Resolver compatibilidade de runtimes e bibliotecas no M0 e incluir lockfiles.
- Langfuse pode ser serviço configurado pelo operador ou perfil local opcional. O modo básico deve funcionar sem depender da disponibilidade desse serviço.
- AWS é a cloud escolhida para evitar multiplicar infraestrutura. Terraform e AWS são obrigatórios na preparação da entrega; criação de recursos depende de credenciais e orçamento autorizados.

## Evidência de competência

Criar `docs/skills-evidence.md` com uma linha por eixo: requisito, código que o implementa, teste/comando, resultado real e limitação. No README, apresentar apenas capacidades comprovadas. Um protótipo local não deve ser descrito como sistema de produção com usuários reais.

## O que priorizar

O usuário deve conseguir explicar chunking, recuperação, seleção de contexto, falhas de ferramentas, custo, avaliação e consistência de arquivos. A IA implementadora deve escrever ADRs com alternativas e resultados e preparar exemplos reproduzíveis que permitam ao usuário estudar e defender essas decisões.
