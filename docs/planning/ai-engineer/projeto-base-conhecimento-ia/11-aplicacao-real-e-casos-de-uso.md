# Aplicação real, motivos de uso e validação

Atualizado em 11/11/2026. Origem: discussão com o usuário sobre a utilidade da aplicação. Os cenários abaixo são exemplos ilustrativos de uso proposto; não comprovam demanda, adoção, economia de tempo ou redução de erros.

## Promessa de uso

**Adicione uma mudança, decisão ou pesquisa e receba propostas de atualização para a documentação afetada, com fontes e revisão.**

A tarefa atendida é manter informações coerentes quando chega material novo. Hoje, a pessoa precisa lembrar quais documentos existem, localizar trechos relacionados, comparar afirmações, preparar alterações e conferir o resultado. A hipótese é que o produto reduza esse trabalho sem retirar a decisão de quem mantém a base.

RAG, agentes e interface própria são meios de executar essa tarefa. Para o usuário final, os resultados relevantes são encontrar os documentos certos, revisar mudanças úteis e conseguir verificar sua origem. Para o portfólio, importa demonstrar como esses resultados foram implementados e medidos.

## Quem teria motivo para usar

| Público potencial | Situação recorrente | Benefício a validar |
|---|---|---|
| Responsável pela documentação de um projeto | Uma decisão técnica afeta manuais, onboarding e troubleshooting | Localizar trechos afetados e preparar correções com menos esforço |
| Pesquisador, estudante ou profissional que acompanha um tema | Novas fontes complementam ou contradizem notas existentes | Incorporar descobertas preservando evidências e divergências |
| Responsável por uma base de suporte | Um procedimento muda e instruções anteriores continuam circulando | Revisar a base e reduzir o risco de consultar uma orientação antiga |

Essas personas são hipóteses. Na v1, cada uma pode ser atendida por um operador usando uma pasta Markdown; não é necessário um SaaS próprio, integração com help desk ou colaboração simultânea.

## UC01 — Uma decisão técnica afeta vários documentos

**Ator:** desenvolvedor responsável por manter a documentação de um projeto pequeno.

**Situação inicial:** `deploy.md` instrui executar o comando fictício `deploy.sh`; `onboarding.md` repete o procedimento; `troubleshooting.md` orienta como resolver erros desse script. Uma nova decisão em Markdown estabelece que deploys passam a ser feitos por workflow, com aprovação do responsável. O exemplo descreve texto documental; a aplicação não executa comandos ou configura CI.

**Gatilho:** o usuário importa a decisão e pede: “Encontre instruções afetadas e prepare atualizações”.

**Fluxo esperado:**

1. Preservar a decisão como fonte versionada e recuperar os trechos relacionados nas três notas.
2. Exibir os documentos possivelmente afetados, trechos antigos e evidência que justifica cada relação.
3. Preparar uma proposta independente por documento, mantendo o limite de um alvo por proposta da v1.
4. Mostrar diff e fonte ao lado de cada alteração. Informações ausentes, como o nome exato do workflow, viram lacunas a esclarecer; não inventar passos operacionais.
5. Permitir editar, aprovar ou rejeitar cada proposta. Aplicar apenas alvos aprovados e ainda atuais; em pasta externa, exportar as propostas.
6. Manter histórico da decisão, aprovações e revisões. Mostrar propostas restantes mesmo que algumas tenham sido rejeitadas.

**Exemplo de saída:** “Três documentos contêm instruções relacionadas ao procedimento anterior. Duas alterações estão prontas para revisão; a terceira depende de informar como acionar o novo workflow.”

**Benefício esperado:** economizar procura/comparação/edição e reduzir a possibilidade de alguém seguir um procedimento antigo. A ferramenta identifica candidatos a atualização; não garante encontrar todos os documentos nem determina sozinha que uma instrução é inválida.

**Aceite do cenário:** o corpus de teste identifica previamente os três alvos e inclui uma nota semelhante, mas não afetada. Verificar recuperação dos alvos, preservação de conteúdo relevante, sinalização da lacuna e ausência de alteração da nota não afetada. Avaliar falsos positivos e falsos negativos, não apenas uma saída convincente.

## UC02 — Atualizar pesquisas e um plano pessoal de estudos

**Ator:** pessoa que mantém pesquisas sobre vagas de AI Engineer e um plano de preparação.

**Situação inicial:** existem dois relatórios sobre requisitos de vagas e uma nota derivada com prioridades de estudo. Algum tempo depois, a pessoa importa uma nova pesquisa. O exemplo usa esse tema por já existir no contexto do usuário; nenhuma mudança concreta do mercado é presumida aqui.

**Fluxo esperado:** recuperar relatórios e plano relacionados; destacar o que a fonte nova acrescenta, repete ou contradiz; preparar propostas para uma nota de síntese e, quando sustentado, para o plano. Uma fonte mais recente não invalida automaticamente a anterior, e uma amostra pequena não justifica afirmar uma tendência de todo o mercado.

**Preservação:** relatórios datados podem ser configurados como fontes imutáveis. Nesse caso, propor uma nova síntese ou adendo em vez de reescrever o registro histórico. Isso pode usar a política de pastas somente leitura já prevista na configuração; não exige alteração automática das regras do vault.

**Exemplo de saída:** “A nova fonte acrescenta uma competência à amostra consultada. Sugiro registrá-la na síntese como observação dessa fonte. Não há evidência suficiente para mudar sua prioridade de estudo automaticamente.”

**Benefício esperado:** aproveitar o conhecimento acumulado e manter a ligação entre fonte, interpretação e plano. Se a pesquisa apenas repetir o conteúdo existente, `no_change` é resultado útil.

**Aceite do cenário:** manter relatórios protegidos intactos, propor apenas conteúdo sustentado, diferenciar observação de recomendação e apresentar referências verificáveis. Testar também repetição e divergência entre fontes.

## Outros usos dentro do mesmo fluxo

| Caso | Entrada em Markdown | Saída proposta |
|---|---|---|
| UC03 — Procedimento de suporte | Comunicado com novo procedimento aprovado | Atualização de FAQ e roteiro, em propostas separadas, preservando exceções documentadas |
| UC04 — Decisão de reunião | Ata explicitando decisão e responsável | Proposta de atualização do manual, distinguindo decisões de assuntos ainda em discussão |
| UC05 — Revisão de literatura | Notas de uma nova fonte com referências | Acréscimo à síntese, incluindo limitações e divergências sem tratá-las como resolvidas |

Esses exemplos não adicionam integrações obrigatórias. A v1 recebe conteúdo explicitamente importado/configurado. Detectar mudanças sozinho em sites, reuniões, código ou ferramentas externas exige conectores futuros e autorização própria.

## Diferença em relação ao fluxo atual

No contexto observado, o usuário usa Obsidian, arquivos Markdown, instruções para agentes e Git. O projeto propõe transformar a procura e a atualização em um fluxo de produto: recuperação de evidências, propostas estruturadas, revisão de versões e medição de qualidade. A comparação deve usar esse processo real, incluindo assistência por IA quando já fizer parte dele; comparar só com edição manual pode exagerar o ganho.

Ter outra interface ou usar RAG não prova vantagem por si só. O custo de instalar, indexar, revisar sugestões ruins e manter a aplicação precisa entrar na avaliação.

## Quando o benefício pode ser pequeno

- Poucas notas, raramente atualizadas, que a pessoa encontra facilmente.
- Uso voltado apenas a escrever e arquivar, sem necessidade de conciliar fontes.
- Informações novas que não afetam documentos existentes.
- Processo atual que já resolve a tarefa com menos esforço que instalar e revisar esta ferramenta.
- Ausência de fontes verificáveis ou de uma pessoa capaz de avaliar a correção das mudanças.

O problema de “encontrar uma nota” é diferente de “atualizar documentação afetada”. A busca apoia ambos, mas esta proposta prioriza o segundo. Se a validação apontar que a dor principal é apenas busca, registrar a conclusão e discutir mudança de foco antes de ampliar o escopo.

## Protocolo inicial de validação de utilidade

1. Selecionar até dez mudanças recentes que o usuário realmente precisou incorporar, buscando completar dez quando disponíveis. Registrar origem, frequência, documentos afetados e trabalho necessário. Se não houver casos, tratar recorrência da dor como não confirmada.
2. Preparar cópias/snapshots autorizados e uma referência humana do que deveria mudar. Manter notas irrelevantes e exemplos em que nenhuma atualização seja necessária.
3. Registrar o processo habitual de resolver tarefas comparáveis, incluindo ferramentas de IA já utilizadas. Medir tempo de localizar, comparar, editar e conferir, além de erros e retrabalho.
4. Repetir tarefas equivalentes com o protótipo, contabilizando ingestão, espera, revisão e correção. Ao repetir o mesmo caso, reconhecer o efeito de aprendizado; alternar ordem entre participantes ou usar conjuntos equivalentes quando possível.
5. Contar documentos afetados encontrados, candidatos incorretos, mudanças indevidas e propostas aceitas/editadas/rejeitadas, com justificativas. Aceitação sozinha não prova correção: conferir resultado contra a referência humana.
6. Registrar feedback de participantes que tenham essa tarefa e consentiram em testar. Distinguir observação do próprio autor, feedback externo e dados sintéticos.
7. Escrever `docs/product-validation.md` com amostra, procedimento, resultados por caso, limitações e decisão sobre manter ou ajustar o foco. Ausência de casos/participantes deve constar como validação pendente, sem impedir testes técnicos com fixtures.

## Como interpretar e apresentar o resultado

O sinal favorável é reduzir esforço total mantendo qualidade e rastreabilidade em tarefas que se repetem. Se revisar e corrigir custar mais que o processo habitual, investigar a causa ou reduzir o escopo. Não há meta de economia comprovada nem evidência de disposição a pagar neste planejamento.

Para o portfólio, mostrar uma necessidade concreta, o fluxo executado, resultados comparados e limitações. Métricas técnicas de RAG do [documento 07](07-avaliacao-e-testes.md) e validação de utilidade respondem perguntas diferentes; apresentar ambas. Manter as tecnologias obrigatórias de [02](02-stack-e-empregabilidade.md) ligadas a comportamentos testáveis, sem usar quantidade de ferramentas como substituto do benefício ao usuário.
