# Operação, observabilidade e implantação

## Jobs

Usar Celery/Redis para execução e PostgreSQL para estado durável. Configurar acknowledgements, timeout, retries e recuperação de worker perdido conscientemente, com testes na versão fixada. Retry/acknowledgement não garantem execução exatamente uma vez; projetar tarefas idempotentes. [Documentação Celery](https://docs.celeryq.dev/en/stable/userguide/tasks.html).

Separar filas de ingestão e tarefas interativas. Configurar concorrência, tamanho máximo de fila, quotas por workspace e rate limit de provedor. Usar backoff exponencial com jitter para erros transitórios; autenticação inválida/schema incompatível falham sem repetição infinita.

Job deve ter heartbeat/lease e reconciliador para execuções abandonadas. Dedupe protege revisão/configuração já processada. Um cancelamento impede novas etapas e é distinguido de uma operação já concluída. Cancelamento na aplicação de arquivo espera o resultado determinístico do journal antes de reportar estado.

## Observabilidade

Propagar `trace_id`, `run_id`, `job_id` e `workspace_id` entre API, outbox, worker, grafo, retrieval e chamadas de modelo. Instrumentar tempos, filas, erros e retries com OpenTelemetry; integrar traces e avaliações de IA ao Langfuse usando a API/SDK compatível. Evitar spans duplicados por instrumentação sobreposta. [Referência](https://langfuse.com/integrations/native/opentelemetry).

Registrar modelo, versão de prompt, tokens reportados, estimativa de custo, latência, chunks recuperados e validações. Valores indisponíveis devem ser `unknown`, nunca zero fabricado. Custos estimados usam tabela datada e separada de cobrança real; incluir geração, embeddings, juiz e retries.

Painel mínimo: execuções por estado, erros por tipo, duração p50/p95, uso por workspace, fila pendente e propostas aceitas/editadas/rejeitadas. Prompts e conteúdo integral ficam fora dos logs padrão. Falha do exportador de telemetria não deve impedir salvar uma nota.

## Instalação local

Docker Compose deve iniciar web, API, worker, PostgreSQL/pgvector e Redis com volumes persistentes. Fornecer perfil opcional para observabilidade local ou configurar endpoint existente; não embutir toda infraestrutura do Langfuse no perfil mínimo sem necessidade.

Entregar `.env.example` sem credenciais, migrations, seed de demo, health/readiness checks e comandos documentados. Uso de modelo real requer configuração explícita; sem ela, leitura/edição/busca textual funcionam e capacidades dependentes de embeddings/LLM ficam claramente indisponíveis.

A pasta externa é montada read-only. Conteúdo gerenciado, snapshots e banco recebem volumes separados. Atualização de imagem deve preservar dados. Documentar exportação, backup, restauração e remoção do ambiente sem apagar dados por acidente.

## CI/CD

GitHub Actions: lint, tipos, testes unitários, integrações com serviços reais, Playwright crítico, build de imagens e verificação de migrations. Publicar artefatos de teste; só publicar imagem de release após checks obrigatórios. Fixar identificadores de imagens/ações e documentar política de atualização.

Medições com modelos reais rodam em workflow manual/autorizado ou agenda com orçamento configurado. Contribuições externas não recebem segredos. Falta de credenciais deve aparecer como validação não executada, e não como aprovação do teste.

## AWS de referência

Escolha inicial econômica e operacionalmente simples: uma instância EC2 com Docker Compose, armazenamento EBS persistente criptografado, IAM com privilégios mínimos, S3 privado para backups, logs operacionais e HTTPS. Tipo de instância, região, domínio e retenção são variáveis, não constantes arbitrárias.

Terraform deve declarar recursos, outputs e instruções de teardown. Evitar credenciais estáticas no repositório; preferir identidade de workload/role e secret store. Banco e Redis não ficam publicamente acessíveis. Configurar limite/alerta de orçamento e quotas da aplicação antes de abrir a demo; alertas financeiros não são um bloqueio automático de gastos.

Esse perfil demonstra cloud e IaC, mas tem ponto único de falha. Não alegar alta disponibilidade. RDS, armazenamento compartilhado, workers em múltiplos hosts e Kubernetes são evolução condicionada a necessidade e medições.

Preparar configuração e validações sem criar recursos pagos. Provisionar apenas com credenciais e orçamento autorizados pelo operador. Para evidência completa de cloud, executar deploy real, smoke test, recuperação e teardown; caso não autorizado, registrar esse item como pendente, mantendo o pacote pronto para execução.

## Demonstração pública

Usar dados públicos/sintéticos. Oferecer sessão efêmera por visitante e isolamento entre workspaces, com rate limits e orçamento por sessão. Uma alternativa aceitável é demo navegável de resultados gravados claramente rotulados, acompanhada de execução real em vídeo; ela não substitui o teste real de integração.

Um usuário remoto pode importar arquivos explicitamente; o servidor não deve oferecer acesso ao filesystem do visitante ou ao vault do mantenedor. Evitar anonimato com operações caras ilimitadas. A UI apresenta a origem dos dados e se a execução é gravada ou ao vivo.

## Backup e recuperação

Backup deve abranger PostgreSQL, conteúdo Markdown ativo, snapshots, configurações de índice e journals. Criar procedimento consistente com quiescência de escrita ou ponto de recuperação documentado. Testar restauração em ambiente vazio e verificar hashes, referências e estado das propostas. Recriar embeddings é possível; perder auditoria sem backup não é.

Runbook obrigatório: modelo indisponível, fila parada, disco cheio, PostgreSQL indisponível, índice incompatível após troca de modelo, operação `needs_reconciliation` e orçamento esgotado. Cada procedimento informa detecção, ação, recuperação e validação.

## Evidências de entrega

README com instalação testada; Compose funcional; CI verde; relatório de falha/recuperação; trace sanitizado de um fluxo completo; Terraform validado; resultado de deploy real ou bloqueio externo explicitado; custo observado da demo e instruções de desligamento. Não publicar segredos nem exemplos contendo dados pessoais.
