# Requisitos de AI Engineer — recorte Brasil

Pesquisa em 10/11/2026. Amostra intencional de sete anúncios de empresas diferentes: seis descrições lidas integralmente nas páginas oficiais/ATS e uma descrição obtida integralmente no índice de busca da própria página (CI&T; abertura direta retornou 403). Não é levantamento estatístico do mercado nem comprovação da data de publicação. O recorte privilegia IA aplicada/GenAI; não representa toda a engenharia de ML, visão computacional ou pesquisa. Ausência no anúncio não significa ausência na seleção. As classificações abaixo descrevem requisitos, responsabilidades e diferenciais separadamente.

## Vagas consultadas

### 1. Arena — AI Engineer

[Anúncio oficial](https://job-boards.greenhouse.io/arenaim/jobs/4740889005). São Paulo; mínimo de dois anos em AI/ML/software engineering. Exige Python, software em produção, LLMs/APIs, avaliação, prompts, cloud/sistemas distribuídos e inglês fluente. A experiência em aplicações cita RAG, embeddings, bancos vetoriais, agentes **ou** tool calling; não exige explicitamente todos em conjunto. Diferenciais: LangChain/LangGraph, TypeScript, AWS/serverless e tecnologias de dados. Não exige diploma na lista de requisitos.

### 2. BEES/AB InBev — AI Engineer

[Anúncio oficial](https://job-boards.greenhouse.io/bees/jobs/8868236002). Campinas/SP; nível não rotulado. Obrigatórios: Python e C++/Go para componentes críticos, experiência com LLMs, orquestração de agentes, busca/bancos vetoriais, sistemas distribuídos, Kubernetes, otimização de inferência, cloud e infraestrutura como código, segurança de IA. Responsabilidades: multiagentes, RAG, avaliação/observabilidade, CI/CD, latência e throughput. Diferenciais: simulações multiagentes, red-teaming, bancos de grafos, publicações e open source. Não explicita inglês nem titulação acadêmica como requisito. É uma vaga com peso maior em infraestrutura/inferência do que algumas outras da amostra.

### 3. HITSS/Claro Brasil — Engenheiro de IA Generativa

[Anúncio oficial](https://globalhitss.gupy.io/jobs/12758700?jobBoardSource=gupy_public_page). Requer residência em São Paulo e graduação correlata. Exige experiência em engenharia com GenAI, Python, APIs, dados, testes, LLMs, RAG, agentes, avaliação, observabilidade, MCP, infraestrutura e segurança. Inglês intermediário. Pós/mestrado, fine-tuning/serving e certificações são diferenciais. Algumas tecnologias aparecem tanto nos requisitos quanto nos diferenciais; a classificação do anúncio contém sobreposições.

### 4. ioasys — Engenheiro de IA

[Anúncio oficial](https://ioasys.gupy.io/job/eyJqb2JJZCI6MTI3NzY2MTgsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal). Local/modalidade e senioridade não explicitados no texto recuperado. Obrigatórios: base de engenharia de software, Python e/ou TypeScript, GenAI/LLMs/agentes, ferramentas de programação com IA (Claude), APIs, Git/GitHub, CI/CD, PostgreSQL, Linux, Docker, cloud e práticas de teste/depuração. Diferenciais: MCP, RAG, frameworks como LangChain/LangGraph/LlamaIndex, AWS aprofundado, observabilidade, segurança e plataformas compartilhadas. Inglês e diploma não aparecem como exigências. Demonstra que conhecer um framework específico ou RAG pode ser diferencial, dependendo do escopo.

### 5. Vetta — Engenheiro de IA Sênior

[Anúncio oficial](https://vetta.gupy.io/jobs/12826519). Sênior; local/modalidade não explicitados no texto recuperado. Obrigatórios: superior correlato, Python, conhecimento avançado de ML/deep learning/NLP, LLMs, frameworks de orquestração, RAG/busca semântica, bancos vetoriais, cloud, MLOps/monitoramento/governança. Responsabilidades ligadas a documentos jurídicos, privacidade, rastreabilidade e monitoramento em produção. Diferenciais: domínio jurídico/compliance/riscos, setores regulados, certificações Azure/AWS e pós-graduação. Inglês não aparece como requisito explícito. Nesta vaga fundamentos de ML têm peso mais explícito.

### 6. OpenAI — Applied AI Engineer, Digital Natives

[Anúncio oficial](https://openai.com/careers/applied-ai-engineer-digital-natives-sao-paulo/). São Paulo, híbrido três dias/semana. Pede oito ou mais anos de experiência técnica, liderança de sistemas AI/ML em produção e impacto mensurável. Python, JavaScript, TypeScript ou semelhantes são alternativas. Requer julgamento técnico, comunicação com clientes, capacidade de navegar ambiguidade e produzir protótipos com qualidade. Destaca arquitetura de agentes, engenharia de prompts/contexto, avaliação, segurança, confiabilidade, latência, custo e adoção. Não especifica diploma, certificação, framework ou inglês como requisito nessa versão do anúncio. É função aplicada com forte interface com cliente, não uma descrição típica de desenvolvedor interno.

### 7. CI&T — AI Engineer Senior, Brazil [32565]

[Anúncio oficial](https://jobs.lever.co/ciandt/b4f02ee0-09d6-46fc-b0f0-43d55852869a). Brasil remoto; sênior. Conteúdo lido no índice da própria página; acesso direto 403. Requisitos: inglês C1+, experiência extensa de software com Python/FastAPI/async/testes, um ou mais anos de aplicações LLM/agentes chegando a usuários, tool calling/prompts/falhas de modelos, ao menos um framework de agentes, AWS, RAG/embeddings/chunking/busca, CI/CD/Docker/IaC. Responsabilidades incluem SDKs, templates de agentes/MCP, testes de contrato/integração, memória, avaliação e suporte operacional. AgentCore, Terraform e tecnologias específicas aparecem como preferências em trechos do anúncio. Certificações AWS e projetos recentes de agentes podem substituir múltiplos anos de prática segundo o texto, sem dispensar automaticamente os demais requisitos.

## Matriz qualitativa de recorrência

Legenda: R = requisito explícito; A = responsabilidade/escopo; D = diferencial; — = não explicitado. Combinações indicam menções em mais de uma seção. Não são percentuais de demanda do mercado.

Uma célula R pode representar uma competência dentro de alternativas aceitas; não significa que todos os itens agrupados na linha sejam cumulativamente obrigatórios.

| Competência | Arena | BEES | HITSS | ioasys | Vetta | OpenAI SP | CI&T |
|---|---|---|---|---|---|---|---|
| Python (às vezes alternativa a TS/JS) | R | R | R | R | R | R | R |
| LLMs/GenAI | R | R | R | R | R | R/A | R |
| Agentes/orquestração | R/A | R/A | R/A | R/A | R* | R/A | R/A |
| RAG/recuperação/bancos vetoriais | R/A | R/A | R/A | D | R/A | — | R/A |
| Avaliação específica de IA | R/A | A | R/A | — | A | R/A | A |
| Operação/monitoramento/produção | R/A | R/A | R/A | R/A | R/A | R/A | R/A |
| Cloud | R | R | D | R | R | — | R |
| Docker/Kubernetes ou CI/CD | — | R/A | R | R | — | — | R |
| Segurança/governança | — | R/A | R/A | D | R/A | R/A | A |
| Inglês explicitamente requerido | Fluente | — | Intermediário | — | — | — | C1+ |
| Graduação explicitamente requerida | — | — | R | — | R | — | — |
| Pós/certificações | — | — | D | — | D | — | D |
| Fine-tuning | — | — | D | — | — | — | — |

*Vetta lista frameworks de orquestração, mas não explicita sistemas de agentes como competência separada; não usar esta célula para contar vagas que exigem experiência em agentes.

## Interpretação

O núcleo recorrente é construir software com modelos e colocá-lo em produção: programação, integração, recuperação de contexto, avaliação e operação. A amostra não sustenta tratar diploma avançado, certificações ou fine-tuning como pré-requisitos universais. Também não sustenta exigir simultaneamente todos os provedores/modelos/frameworks citados. Inglês varia com o contexto: de leitura técnica na HITSS a fluência na Arena e C1 na CI&T. Experiência anterior de software aparece como porta de entrada explícita; os anos pedidos variam bastante e não devem ser confundidos com anos exclusivamente em GenAI.

As interpretações derivam dos sete anúncios acima e devem ser usadas para orientar prioridades, sem extrapolar frequências populacionais ou concluir que vagas juniores inexistem.
