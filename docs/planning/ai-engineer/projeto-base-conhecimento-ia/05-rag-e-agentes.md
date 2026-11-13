# RAG, contexto e agentes

## Ingestão incremental

1. Validar arquivo, tamanho, caminho, permissão e exclusões; capturar snapshot e hash.
2. Extrair título, headings, frontmatter e links preservando o Markdown original.
3. Dividir por seções e limites de tokens, preservando blocos de código/tabelas quando viável. Ponto inicial de experimento: chunks de 400–800 tokens e overlap limitado; decidir pelo conjunto de desenvolvimento.
4. Registrar trecho, offsets e revisão de origem. Identidade do chunk deriva de documento, revisão, parser e posição; não deduplicar identidade de documentos apenas por texto igual.
5. Gerar embeddings em batches, respeitar rate limits e permitir retomada. Cache de embeddings pode usar hash do trecho + configuração, com separação por workspace por padrão.
6. Ativar a nova revisão do índice apenas após completar seus chunks. Revisões antigas permanecem para evidências históricas, mas ficam fora da busca corrente.

Deduplicação de conteúdo idêntico reduz processamento, sem perder origem. Se parser/modelo/dimensão mudar, criar uma nova configuração de índice e reindexar antes da troca; não misturar espaços vetoriais.

## Recuperação

Implementar três modos comparáveis: textual, vetorial e híbrido. No híbrido, fundir rankings com Reciprocal Rank Fusion; não somar diretamente scores de escalas diferentes. Configurar idioma do full-text para PT/EN ou `simple` para conteúdo técnico, justificando em experimento.

Filtros de workspace, permissões, status e revisão ativa devem preceder a geração de contexto. `limit` é limitado no servidor. Resultados incluem referência, seção, trecho e scores internos para depuração; scores não são probabilidade de verdade.

Começar com busca exata para corpus pequeno e medir HNSW quando necessário. Verificar comportamento de filtros e recall na versão escolhida do pgvector. Reranking é um experimento opcional: adicionar somente com comparação de qualidade, custo e latência.

## Construção de contexto

Separar instruções da aplicação, pergunta, fontes recuperadas e conteúdo-alvo. Documentos são dados não confiáveis; instruções contidas neles não alteram políticas nem ferramentas disponíveis.

Selecionar trechos sem duplicação excessiva e conservar título, data disponível e revisão. Reservar orçamento para resposta e ferramentas. Registrar chunks selecionados, configuração e versão do prompt para reprodução, respeitando política de retenção.

Propostas pendentes/rejeitadas não são fonte factual para novas respostas. Fontes importadas podem ser evidência com proveniência explícita; notas aprovadas não são automaticamente verdadeiras. Divergências exigem mostrar ambas as fontes; data recente, isoladamente, não decide qual afirmação é correta.

## Fluxo LangGraph obrigatório

```text
validate_input → retrieve → inspect_sources → plan → draft_structured
→ validate_citations_and_patch → [repair limitado | no_change | needs_evidence]
→ persist_proposal → interrupt_for_review
→ resume_with_decision → [reject | revalidate_edited_version | authorize_apply]
→ enqueue_apply → await_result
```

O grafo deve usar checkpoint durável no PostgreSQL, `thread_id` escopado ao workspace e estados tipados. Durante espera humana, persistir estado e liberar worker; não manter processo bloqueado. Ao retomar, conferir identidade, versão e decisão no domínio antes de continuar.

LangGraph pode reexecutar trechos de nós na retomada. Ferramentas e efeitos devem ser idempotentes; não colocar gravação de arquivos antes de uma interrupção esperando que rode exatamente uma vez. Ver [documentação de interrupções](https://docs.langchain.com/oss/python/langgraph/interrupts).

## Ferramentas disponíveis ao agente

| Ferramenta | Papel e limite |
|---|---|
| `search_documents(query, filters)` | Recuperar evidências autorizadas, limite de resultados |
| `read_document_revision(id, revision)` | Ler snapshot autorizado com limite de tamanho |
| `get_document_links(id)` | Consultar relações explícitas; sem inferir verdade por conexão |
| `compare_revisions(base, target)` | Gerar comparação determinística de conteúdo |
| `submit_proposal(payload)` | Validar e persistir proposta; sem aplicar arquivos |

Implementar ao menos um caminho real de tool calling pelo modelo para escolher consultas ou ler fontes adicionais. Manter número de chamadas limitado e a transição de aplicação sob controle determinístico. O LLM não recebe ferramenta de shell, acesso arbitrário à rede ou escrita irrestrita no filesystem.

## Validação de saída

- Pydantic valida schema e campos permitidos; IDs de documentos e citações precisam existir no workspace.
- Validar que citações apontam para trechos presentes no snapshot. A existência do trecho não garante que ele sustente a afirmação: usar checagem semântica e revisão humana.
- Impedir proposta sobre revisão-base diferente da lida; marcar conflito quando a fonte relevante ou o alvo mudar antes da aprovação/aplicação.
- Mostrar conteúdo removido, não apenas adicionado. Remoções substanciais devem ser destacadas para revisão.
- Nenhuma atualização necessária é um resultado válido. Falha de schema, referência inválida ou falta de suporte factual deve produzir erro/insuficiência explícitos.
- Aceitar texto editado pelo usuário como conteúdo de autoria humana, distinguindo-o de afirmação validada por IA. Revalidar referências e revisão-base; retirar selos de suporte não comprovado.

## Limites iniciais configuráveis

Até 8 chamadas de ferramenta por run, 2 tentativas de reparo de saída e 3 retries de falhas transitórias com backoff/jitter. Definir timeout por chamada e deadline por execução no M0. O orçamento em tokens e moeda depende do modelo e deve ser configurado e exibido antes de operações grandes.

Tratar `429`, timeout, indisponibilidade, saída inválida, contexto excedido e cancelamento. Troca de modelo deve registrar a mudança e não contornar consentimento sobre provedor. Cancelamento interrompe novas etapas; se a operação já foi aplicada, oferecer restauração em vez de declarar que foi cancelada.

## MCP obrigatório no M7

Expor `search_knowledge`, `read_evidence` e `get_proposal` via SDK oficial e transporte local stdio. Reutilizar autorização e serviços do domínio. Configurar um principal/workspace limitado para o processo e registrar protocolo sem conteúdo sensível em stderr; stdout é reservado às mensagens MCP. Ferramentas MCP da v1 são somente leitura e não aprovam/aplicam propostas. Testar com cliente compatível e documentar configuração reproduzível. [Referência](https://modelcontextprotocol.io/docs/develop/build-server).
