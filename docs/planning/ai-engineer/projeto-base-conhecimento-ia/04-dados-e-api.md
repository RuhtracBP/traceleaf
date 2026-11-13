# Modelo de dados e contratos

## Convenções

IDs opacos UUID, timestamps UTC, hashes SHA-256 do conteúdo exato e payloads validados com Pydantic. `workspace_id` é obrigatório em entidades de domínio e filtros. Autorização ocorre no servidor; receber um workspace no request não prova acesso. Conteúdo de notas permanece separado de logs operacionais.

## Entidades mínimas

| Entidade | Campos e invariantes essenciais |
|---|---|
| Workspace | id, owner, name, mode, storage_root_ref, settings; modo gerenciado ou externo somente leitura |
| Membership | principal_id, workspace_id, role; ao menos owner e reader; identidade local também tem principal |
| Document | id, workspace_id, relative_path, title, current_revision_id, state, index_status; caminho único por workspace |
| Revision | id, document_id, content_hash, snapshot_ref, created_at, actor, origin; conteúdo imutável e anterior recuperável |
| Source | id, workspace_id, revision_id, origin, imported_at, observed_date, trust; origem externa é dado, não instrução |
| Chunk | id, workspace_id, revision_id, heading_path, offsets, content_hash, parser_version, embedding_config_id, vector, tsvector |
| EmbeddingConfig | provider, model_id, dimension, normalization, version; vetores incompatíveis nunca são comparados |
| Citation | id, workspace_id, revision_id, chunk_id/offsets, quote_hash; aponta para snapshot verificável |
| Run | id, workspace_id, actor_id, thread_id, config_hash, prompt_version, state, usage, trace_id |
| Proposal | id, workspace_id, run_id, target_document_id ou new_path, base_revision_id, version, content_hash, status |
| ProposalClaim | proposal_version, claim_id, summary, citation_ids, evidence_status; associação entre afirmação e suporte |
| Approval | id, proposal_id, proposal_version, proposal_hash, actor, timestamp; inválida após edição da proposta |
| ApplyOperation | id, proposal_id/version, base_hash, intended_hash, stage, result_revision_id, idempotency_key |
| Job / OutboxEvent | id, workspace_id, type, dedupe_key, status, attempts, lease_until, next_attempt_at, payload_ref |
| AuditEvent | workspace_id, actor, action, target_id, before_ref, after_ref, timestamp, trace_id; append-only |

Snapshots podem morar em armazenamento por conteúdo fora da árvore de notas ativas. Não injetar IDs proprietários no frontmatter para fazer o sistema funcionar. Identidades vivem no banco; exportação continua legível.

## Estados

- Job: `queued → running → succeeded | failed | cancelled`; estado adicional `waiting_review` para fluxo pausado. Retry reabre job com tentativa incrementada e histórico preservado.
- Proposal: `draft → awaiting_review → approved → applying → applied`.
- De `awaiting_review`, aceitar edição (nova versão) ou `rejected`; editar após aprovação revoga Approval e volta a `awaiting_review`.
- Revisão-base divergente leva a `conflicted`; regeneração cria nova versão e nova revisão humana.
- Falha de aplicação leva a `apply_failed` ou `needs_reconciliation`; retomada reaproveita ApplyOperation, não cria nova mudança sem verificar o resultado anterior.
- Uma execução sem atualização retorna resultado `no_change`; não gera aprovação vazia.
- Uma restauração cria nova revisão com evento `restore`; a proposta antiga continua historicamente aplicada.

## API REST inicial

Prefixo `/api/v1`. Operações de workspace usam `/workspaces/{workspace_id}`; o servidor resolve todos os IDs dentro desse escopo.

| Método e rota relativa | Contrato |
|---|---|
| `GET /workspaces`, `POST /workspaces` | Listar/criar espaços permitidos; modo externo exige configuração de raiz pelo operador |
| `GET /documents` | Cursor, pasta, tags, status; retorna itens e `next_cursor` |
| `POST /imports` | Upload `.md`/texto, limites e proveniência; retorna `202`, `job_id` |
| `POST /sync` | Reconciliar raiz configurada; somente local/admin; retorna job |
| `GET /documents/{id}` | Conteúdo, revisão e `ETag` igual ao hash de conteúdo |
| `POST /documents` | Criar nota gerenciada com path relativo validado e política create-only |
| `PUT /documents/{id}` | Corpo Markdown e `If-Match`; conflito retorna `409` com revisão atual |
| `POST /documents/{id}/move` | Novo path relativo, revisão esperada e preview das referências afetadas |
| `POST /documents/{id}/archive` | Arquivar com revisão esperada; removido da recuperação ativa |
| `GET /documents/{id}/revisions` | Histórico paginado e acesso autorizado ao snapshot |
| `POST /documents/{id}/restore` | Revisão histórica e revisão atual esperada; cria uma nova revisão |
| `POST /search` | query, filtros, modo, limit; retorna evidências versionadas e modo de busca usado |
| `POST /answers` | Pergunta e filtros; retorna run/job; resultado contém afirmações e citações |
| `POST /proposals` | source_ids, objetivo opcional; retorna run/job; documentos vêm do workspace |
| `GET /proposals/{id}` | Versão, status, diff, conteúdo completo proposto, fontes e bloqueios |
| `PATCH /proposals/{id}` | Editar usando versão esperada; revalidar fontes, revogar aprovação antiga |
| `POST /proposals/{id}/approve` | Versão/hash vistos pelo usuário; cria Approval se ainda válidos |
| `POST /proposals/{id}/apply` | Exige Approval e `Idempotency-Key`; enfileira aplicação ou retorna resultado já existente |
| `POST /proposals/{id}/reject` | Versão e motivo opcional; mantém histórico |
| `GET /jobs/{id}`, `POST /jobs/{id}/cancel` | Estado, progresso, resultado/erro; cancelamento cooperativo |
| `GET /events` | SSE opcional com cursor para atualização da UI; polling permanece fallback |
| `GET /citations/{id}` | Snapshot/trecho autorizado; marcar se nota atual mudou ou foi arquivada |
| `POST /exports` | Gerar pacote de Markdown/proposta; download limitado ao workspace |

Os endpoints relativos acima são anexados ao prefixo de workspace, exceto a listagem/criação de workspaces. Gerar OpenAPI e tipos do frontend a partir dos contratos reais.

## Schemas de IA

Resposta: `{status: answered|insufficient_evidence, claims: [{text, citation_ids}], gaps: []}`. Status e referências são validados antes de exibir o resultado final.

Proposta: `{action: create|update|no_change, target_document_id, new_path, base_revision_id, proposed_markdown, claims: [{id, summary, citation_ids}], conflicts: [{description, citation_ids}], rationale_summary}`. Campos aplicáveis dependem de `action`; usar união discriminada.

O backend calcula o diff entre snapshot-base e `proposed_markdown`. O modelo não escolhe caminhos absolutos nem executa patches de shell. JSON válido não prova suporte factual: aplicar validadores e avaliação de [05](05-rag-e-agentes.md) e [07](07-avaliacao-e-testes.md).

## Erros e idempotência

Envelope: `{error: {code, message, retryable, trace_id, details}}`; detalhes não expõem segredos. Usar `401/403/404`, `409`, `413`, `422`, `429` e `503` com semântica documentada. Para objetos de outro workspace, preferir resposta indistinguível de objeto inexistente.

Idempotency key é escopada por workspace, principal e operação, associada ao hash do request. Reutilizar a chave com payload diferente retorna conflito. Respostas e jobs duplicados retornam o mesmo resultado lógico. Unique constraints devem proteger essas invariantes, além das verificações de aplicação.
