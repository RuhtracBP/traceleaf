# Começar com o Traceleaf

Esta entrega inicia o **M0**: a interface consulta o estado real da API, PostgreSQL/pgvector e Redis. Biblioteca/editor chegam no M1; RAG no M2; propostas com revisão no M3. Nenhum vault pessoal é conectado e não há chamadas a modelos.

Na raiz do projeto, com Docker/Compose em execução e Python 3 instalado:

```sh
python3 scripts/setup_env.py
docker compose up --build --wait
```

Abra **http://localhost:8080**. A documentação da API fica em **http://localhost:8000/docs**. O primeiro build baixa imagens e dependências. A configuração gera uma senha aleatória para o banco local; mantenha `.env` fora do Git. Se as portas estiverem ocupadas, altere `TRACELEAF_WEB_PORT` e `TRACELEAF_API_PORT` nesse arquivo.

Para parar sem apagar os dados: `docker compose down`. Para ver erros: `docker compose logs --tail=80 api migrate web`. `docker compose ps` mostra a saúde dos serviços. Não use `down --volumes` na instalação principal se quiser preservar os dados.

Para desenvolver, use Python 3.12.16, Node 26.13.1, uv 0.13.8 e pnpm 12.18.0. Execute `make setup`, `make check` e `make integration`. A integração usa serviços reais em um projeto Docker separado e descarta apenas os dados de teste. Com o app no ar, execute `pnpm exec playwright install chromium` e `make e2e`.

As instruções de hot reload e os detalhes de configuração estão no [README](../README.md). A instalação atual é local: autenticação e acesso a documentos serão implementados juntos no M1. Não publique esta fundação como uma aplicação multiusuário.

O próximo marco deve seguir RF01–RF05, RF12 e RF14 do [planejamento](planning/ai-engineer/projeto-base-conhecimento-ia/09-plano-de-implementacao.md): identidade e autorização, workspaces, importação, leitor/editor, histórico e exportação. Use o corpus sintético UC01 e pastas descartáveis para validar escrita e isolamento.
