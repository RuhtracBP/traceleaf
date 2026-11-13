# Integridade de arquivos, revisão e segurança

## Fronteiras de acesso

Configurar raiz por workspace e resolver caminhos relativos sob essa raiz. Rejeitar traversal, paths absolutos recebidos do cliente, symlinks que escapem, colisões e arquivos especiais. Validar novamente no acesso ao arquivo; validar apenas a string antes da operação não resolve trocas concorrentes de symlink.

Importar apenas Markdown UTF-8 na v1, com limite inicial de 5 MiB por arquivo e limite agregado configurável. Excluir `.git`, `.obsidian`, diretórios de segredos, snapshots internos e padrões configurados. Importar ZIP, seguir links da internet e buscar URLs fornecidas pelo modelo são extensões, não comportamentos implícitos.

Renderização deve sanitizar HTML e bloquear scripts/esquemas perigosos. Imagens remotas ficam bloqueadas por padrão, com abertura explícita. Código em notas é texto; não executar exemplos durante ingestão ou avaliação.

## Autenticação e autorização

Mesmo em modo local, vincular ações a um principal. Binding padrão em loopback, hosts/origens permitidos e sessão autenticada. O bootstrap deve gerar credencial aleatória local e permitir troca por cookie de sessão seguro; nunca usar uma senha padrão pública.

Na demonstração hospedada, exigir HTTPS e sessão isolada. Um visitante pode receber um workspace efêmero com corpus copiado e quotas. Owner edita/revisa; reader apenas consulta. Validar permissões também em jobs, downloads, MCP, citações, checkpoints, cache e eventos SSE.

Cookies HTTP-only, política SameSite e proteção de mutações contra CSRF. Configurar CORS estritamente. Credenciais de provedor vivem no backend/secret store e nunca no bundle frontend, banco em texto puro ou exemplos versionados.

## Protocolo de aplicação

A v1 aplica um documento por operação no modo gerenciado. Uma decisão de aprovação autoriza exatamente uma versão de proposta e sua revisão-base.

1. Receber `Idempotency-Key`, autenticar e carregar Approval, proposta e documento no mesmo workspace.
2. Adquirir exclusão por documento entre escritores da aplicação, com lock PostgreSQL ou mecanismo equivalente testado; garantir unicidade da operação por proposta/versão.
3. Ler bytes atuais e comparar hash com a revisão-base aprovada. Conferir também versões de evidências vinculadas e marcar fontes alteradas para nova revisão. Para criação, exigir ausência do destino.
4. Persistir ApplyOperation `prepared`, snapshot anterior e conteúdo pretendido imutável antes de gravar o arquivo. Preservar original, frontmatter e encoding suportado.
5. Gravar arquivo temporário no mesmo filesystem, sincronizar conforme suporte do SO, revalidar precondição e substituir atomicamente. Na criação, usar operação create-only para impedir overwrite de uma nota criada em paralelo.
6. Confirmar hash resultante, gravar revisão/evento de auditoria e evento de reindexação no banco; finalizar a operação.
7. Reenvio da operação consulta o journal e devolve o resultado existente. Falha após a gravação exige reconciliação, não reaplicação cega.

PostgreSQL e filesystem não formam uma única transação. O journal permite decidir após reinício: hash atual igual ao pretendido → concluir metadados; igual ao anterior → repetir com precondições; diferente de ambos → preservar evidências e marcar `needs_reconciliation`.

Locks da aplicação não bloqueiam Obsidian ou outro processo. Por isso pastas externas são somente leitura na v1. Se o operador editar externamente uma pasta gerenciada, hash/watcher detectam mudanças observáveis, mas não há garantia de compare-and-swap contra escritores não cooperantes. Documentar essa limitação e não prometer sincronização bidirecional segura.

## Restauração, movimentação e auditoria

Restauração usa conteúdo histórico como nova revisão, com hash da versão atual como precondição. Não apagar a história. Arquivamento preserva snapshot e remove o documento da busca ativa. Renomear/mover mantém identidade e registra referências afetadas; alterações em outras notas passam por propostas separadas.

Auditoria registra ator, tipo, IDs, revisões, decisão, horário e trace_id. Mostrar relação fonte → proposta → aprovação → alteração. Uma edição manual posterior não altera retroativamente as evidências da proposta anterior.

## Privacidade e limites da IA

Mostrar quais dados são enviados a qual provedor. Indexação com embeddings externos também envia conteúdo e exige a mesma configuração de consentimento. Oferecer exclusões de pastas e desabilitação de IA remota; leitura/edição continuam funcionando.

Prompts e documentos são dados sensíveis. Logs padrão contêm IDs, duração, contagens e hashes, sem conteúdo integral. Captura detalhada de prompts/respostas exige opção explícita e retenção configurada. Exportações e backups seguem o escopo do workspace; demo pública nunca carrega o vault pessoal.

Prompt injection em fontes não concede permissões. O controle real é autorização, ferramentas limitadas, validação e revisão de escrita, não uma promessa de que um prompt “elimina” ataques.

## Casos obrigatórios de integridade

| Caso | Resultado exigido |
|---|---|
| Aprovar, depois editar a proposta | Aprovação anterior invalidada |
| Editar nota entre proposta e aplicação | Conflito; nenhum overwrite silencioso |
| Duas aplicações concorrentes da mesma proposta | Uma alteração lógica e mesmo resultado idempotente |
| Queda após substituir arquivo, antes de finalizar banco | Reinício reconcilia journal e mantém conteúdo recuperável |
| Queda antes de escrever arquivo | Retry seguro ou falha explícita; conteúdo anterior intacto |
| Caminho fora da raiz ou symlink de escape | Acesso recusado |
| Citação, job ou cache de outro workspace | Sem vazamento de conteúdo, existência ou decisão |
| Documento com instrução para ignorar regras | Sem alteração de permissão, ferramenta ou aprovação |
| Modelo produz alvo/citação inexistente | Proposta bloqueada com erro acionável |
| Usuário restaura revisão após edição recente | Precondição conferida; restauração não elimina auditoria |

Testar em workspaces descartáveis com conteúdo sentinela. Integridade e isolamento têm tolerância zero a falhas conhecidas na entrega, mesmo que métricas de linguagem sejam boas.
