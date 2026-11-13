---
tags: [projeto, ai-engineer, especificacao]
data: 2026-11-10
atualizado: 2026-11-11
tipo: especificacao-para-implementacao
---

# Traceleaf — instruções para a IA implementadora

## Missão

Implemente o **Traceleaf**, uma aplicação própria, open source e viável para manutenção por uma pessoa, que permita ler, organizar e editar arquivos Markdown e incorporar novas informações à base por meio de propostas de IA com fontes, diff e revisão humana. O usuário inicial usa Obsidian; a aplicação também deve funcionar sem ele.

**Objetivo profissional obrigatório:** produzir um projeto demonstrável para candidaturas a AI Engineer. A entrega precisa comprovar engenharia de software, Python, LLMs, RAG, embeddings, agentes com ferramentas, avaliação, operação, segurança e cloud. Cada tecnologia obrigatória deve participar de um fluxo executável, ter testes ou evidência de execução e ser explicada na documentação. Dependência instalada sem uso não satisfaz o requisito.

O nome escolhido pelo usuário é **Traceleaf**. Usar essa grafia na interface, README e materiais do projeto; usar `traceleaf` como identificador técnico quando aplicável. As escolhas de escopo e arquitetura deste pacote são decisões propostas para o projeto, não fatos sobre implementações já existentes. As metas de qualidade e desempenho são objetivos a verificar; nenhum resultado está previamente comprovado.

## Fluxo principal

Promessa de uso: **adicione uma mudança, decisão ou pesquisa e receba propostas de atualização para a documentação afetada, com fontes e revisão.** O benefício esperado é reduzir o trabalho de localizar, comparar e editar informações; a utilidade e a demanda ainda precisam ser validadas. Consulte os exemplos e o protocolo em [11 — Aplicação real e casos de uso](11-aplicacao-real-e-casos-de-uso.md).

`Importar Markdown → recuperar contexto → propor alteração com fontes → revisar diff → aplicar → consultar histórico e desfazer.`

O resultado final deve incluir uma aplicação utilizável, avaliações reproduzíveis, instalação local, demonstração pública com dados próprios para divulgação, infraestrutura de referência e materiais de portfólio em inglês.

## Ordem de leitura

| Quando | Documento obrigatório |
|---|---|
| Antes de planejar ou programar | [11 — Aplicação real e casos de uso](11-aplicacao-real-e-casos-de-uso.md), [01 — Produto e requisitos](01-produto-e-requisitos.md) e [02 — Stack e empregabilidade](02-stack-e-empregabilidade.md) |
| Antes de definir módulos e persistência | [03 — Arquitetura](03-arquitetura.md) e [04 — Dados e API](04-dados-e-api.md) |
| Antes de implementar busca, modelos ou agentes | [05 — RAG e agentes](05-rag-e-agentes.md) |
| Antes de escrever arquivos, autenticar ou expor dados | [06 — Integridade e segurança](06-integridade-e-seguranca.md) |
| Antes de declarar um fluxo concluído | [07 — Avaliação e testes](07-avaliacao-e-testes.md) |
| Antes de executar tarefas assíncronas ou preparar implantação | [08 — Operação e implantação](08-operacao-e-implantacao.md) |
| Para executar o trabalho e verificar a entrega | [09 — Plano de implementação](09-plano-de-implementacao.md) |
| Para justificar escolhas e consultar documentação técnica | [10 — Fontes e contexto](10-fontes-e-contexto.md) |

## Procedimento de execução

1. Inspecione o repositório de destino e suas instruções; preserve trabalho existente. Crie o projeto em repositório próprio, nunca dentro do vault pessoal usado como fonte de pesquisa.
2. Leia os documentos iniciais, selecione o caso de uso inicial conforme [11](11-aplicacao-real-e-casos-de-uso.md) e crie `docs/implementation-status.md` com os marcos M0–M7, status, evidências e pendências. Marque claramente itens não implementados e hipóteses de utilidade ainda não verificadas.
3. Confirme versões compatíveis nas fontes oficiais e fixe dependências e imagens. Registre versões e justificativas em `docs/adr/`; este pacote não fixa versões que podem envelhecer.
4. Execute os marcos em ordem de dependência, entregando fluxos completos de interface a persistência. Ao terminar cada marco, execute seus critérios de aceite e registre comandos e resultados reais.
5. Use fixtures e workspaces temporários nos testes. Para dados reais, só abra pastas explicitamente configuradas pelo operador.
6. Quando faltar credencial, continue tarefas independentes e registre a validação externa pendente. Execute integrações reais assim que houver configuração; mocks não contam como evidência de IA em funcionamento.
7. Ao concluir, publique um relatório de requisitos atendidos, limitações, avaliações, instalação e instruções de demonstração. Separe produto local concluído de validação externa ainda pendente.

## Regras de interpretação

- `DEVE` e a coluna “obrigatório” definem critérios de entrega. “Extensão” descreve evolução posterior, sem bloquear v1.
- Um MVP funcional até M3 não equivale à entrega de portfólio completa M0–M7.
- Escolhas rotineiras de implementação podem ser tomadas pela IA e registradas em ADR. Substituir tecnologia obrigatória ou remover comportamento central exige decisão explícita do responsável pelo projeto.
- Este documento autoriza especificação e implementação futura; não autoriza publicar dados pessoais, conectar o vault real automaticamente ou criar recursos pagos sem autorização do operador.
- Funcionalidades devem executar comportamentos reais. Protótipos de interface, respostas fixas, métricas inventadas e telas de configuração sem integração não satisfazem o aceite.
- A implementação deve justificar decisões e medir limites. “Escalável” só pode ser afirmado para cargas e condições efetivamente testadas.

## Prompt para entregar junto deste pacote

> Implemente o Traceleaf conforme descrito em `00-leia-primeiro.md` e seus documentos vinculados. Meu objetivo é usar a aplicação e apresentá-la em candidaturas a AI Engineer. Comece entendendo a aplicação real e os casos de uso do documento 11; distinga exemplos ilustrativos de benefícios comprovados. Siga a stack obrigatória, implemente fluxos reais, preserve Markdown interoperável, execute avaliações e registre evidências de cada marco. Comece pelo M0 e avance por dependência. Use dados de demonstração compartilháveis; mantenha meu vault pessoal fora dos testes e da publicação. Não considere o trabalho completo apenas porque o MVP ou a interface estão prontos. Se alguma validação depender de credenciais, orçamento ou implantação externa, documente exatamente o que falta e continue as partes independentes.
