# Traceleaf — produto e requisitos

## Problema e público

Pesquisadores individuais e desenvolvedores acumulam notas, documentação e pesquisas em Markdown. Incorporar novas fontes exige localizar conteúdo relacionado, evitar duplicatas, avaliar divergências e editar com rastreabilidade. A aplicação deve reduzir esse trabalho mantendo o usuário no controle das mudanças.

Primeiro usuário: mantenedor de uma base pessoal. Público seguinte: pessoas que mantêm documentação de projetos. A utilidade para outros usuários é uma hipótese a validar, não demanda comprovada.

O motivo de adoção esperado é reduzir o esforço de identificar documentos afetados por uma informação nova e preparar atualizações revisáveis. A proposta faz mais sentido quando o conteúdo muda com frequência e consultar uma instrução antiga tem consequências. Para quem apenas escreve e guarda poucas notas, o benefício pode ser pequeno. Personas, exemplos de entrada/saída e limites estão em [11 — Aplicação real e casos de uso](11-aplicacao-real-e-casos-de-uso.md).

## Modos de uso

- **Gerenciado:** a aplicação administra uma pasta de conteúdo e oferece edição, histórico, aplicação de propostas e restauração. É o modo completo da v1.
- **Pasta externa:** lê uma pasta autorizada, como um vault Obsidian, com sincronização de mudanças e propostas exportáveis. Na v1, é somente leitura; o usuário pode importar uma cópia para o modo gerenciado. Isso evita prometer exclusão mútua com editores externos.
- **Demonstração hospedada:** utiliza corpus público ou sintético e workspaces isolados. Um servidor remoto não tem acesso automático aos arquivos do computador do visitante.

## Requisitos funcionais

| ID | A aplicação DEVE | Aceite observável |
|---|---|---|
| RF01 | Criar, listar e selecionar workspaces | Trocar workspace muda documentos, buscas, propostas e histórico sem misturar dados |
| RF02 | Importar arquivos `.md` e uma pasta configurada no servidor local | Mostrar quantidade, erros por arquivo, duplicatas exatas e progresso |
| RF03 | Exibir árvore de pastas, título, tags e estado de indexação | Navegar, filtrar e encontrar documento sem usar chat |
| RF04 | Ler e editar Markdown no modo gerenciado | Preview seguro, salvar com versão esperada e preservar frontmatter desconhecido |
| RF05 | Criar, renomear, mover e arquivar documentos | Colisões são rejeitadas; referências afetadas são apresentadas para revisão; restauração é possível |
| RF06 | Pesquisar por texto e semântica | Resultado apresenta documento, seção, trecho e acesso à fonte |
| RF07 | Responder perguntas com evidências | Cada afirmação verificável tem referência; ausência de evidência gera resposta de insuficiência |
| RF08 | Receber material como fonte de uma proposta | Fonte ganha snapshot e origem; fica distinguível de nota validada e proposta pendente |
| RF09 | Sugerir criar nota, atualizar nota ou não alterar | Mostrar justificativa curta, evidências e conteúdo proposto; divergências são hipóteses sinalizadas |
| RF10 | Revisar propostas | Visualizar diff, fontes, editar, rejeitar, aprovar e acompanhar aplicação |
| RF11 | Aplicar somente proposta aprovada e atual | Aprovação vincula hash da proposta e revisão-base; conflito impede aplicação silenciosa |
| RF12 | Consultar histórico e restaurar conteúdo | Restauração cria nova revisão e mantém eventos anteriores |
| RF13 | Acompanhar execuções de IA | Exibir progresso, erros úteis, consumo disponível e opção de cancelar |
| RF14 | Exportar a base e propostas | Markdown legível e patches exportados sem exigir o banco da aplicação para leitura |
| RF15 | Configurar uso de modelos externos | Informar destino do conteúdo e permitir excluir pastas/arquivos da indexação e envio |
| RF16 | Usar a aplicação em português | UI inicial pt-BR; código e documentação pública principal em inglês; corpus de avaliação PT e EN |

## Interface

Quatro áreas: biblioteca, editor/leitor, investigação com fontes e fila de revisão. Um painel de execução pode mostrar etapas, tempo, modelo e custo estimado. Mostrar estados vazios, carregamento, erro, falta de credenciais, cancelamento e conflito. A navegação central deve funcionar por teclado, com foco e labels acessíveis.

O editor deve preservar conteúdo Markdown que não consegue interpretar. Renderizar wikilinks, links relativos e frontmatter básico. Suporte a Dataview, plugins, Canvas e todos os dialetos do Obsidian fica fora da v1; elementos não suportados permanecem no arquivo e são indicados na interface.

## Cenários de demonstração obrigatórios

Usar os exemplos UC01 e UC02 do [documento 11](11-aplicacao-real-e-casos-de-uso.md) como contexto dos cenários abaixo. São fixtures ilustrativas, não evidência de adoção real. Cada proposta continua alterando apenas um documento.

1. Uma pesquisa nova complementa uma nota existente; a proposta inclui referências e preserva informações anteriores relevantes.
2. Uma fonte diverge de outra; a ferramenta mostra ambas com datas e propõe registrar a divergência, sem escolher uma verdade automaticamente.
3. Conteúdo já presente resulta em “nenhuma atualização necessária”.
4. A nota é editada depois de gerar a proposta; a aplicação detecta revisão-base desatualizada e exige nova revisão.
5. Uma pergunta não tem evidência suficiente; o sistema explica a lacuna, sem inventar fonte.
6. Uma falha de modelo ou reinício do worker permite recuperar a execução sem aplicar a mesma mudança duas vezes.

## Limites para manter viabilidade solo

Uma proposta altera ou cria um documento por vez. Atualizações de múltiplas notas aparecem como propostas independentes, sem promessa de transação entre arquivos. Renomear mostra links afetados e gera propostas separadas para corrigi-los.

Extensões futuras: escrita compartilhada com Obsidian, colaboração simultânea, ingestão de PDF/OCR e URLs, conectores GitHub, sincronização entre dispositivos, banco de grafos, fine-tuning e marketplace. Kubernetes é extensão de infraestrutura. A v1 não depende dessas funcionalidades.

## Validação de utilidade

Executar o protocolo de [11 — Aplicação real e casos de uso](11-aplicacao-real-e-casos-de-uso.md): selecionar dez mudanças reais quando disponíveis, comparar com o processo habitual, incluir tempo de revisão/correção e registrar também tarefas em que a ferramenta não ajudou. Usar corpus de exemplo para testes técnicos e dados pessoais apenas em workspace autorizado. Resultados técnicos e validação de utilidade devem aparecer separadamente no estudo de caso.
