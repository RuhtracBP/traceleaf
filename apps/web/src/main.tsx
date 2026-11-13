import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { loadOverview } from "./api";
import "./style.css";

type Overview = Awaited<ReturnType<typeof loadOverview>>;
type State =
  { kind: "loading" } | { kind: "error" } | { kind: "loaded"; data: Overview };

function App() {
  const [attempt, setAttempt] = useState(0);
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    setState({ kind: "loading" });
    loadOverview(controller.signal)
      .then((data) => setState({ kind: "loaded", data }))
      .catch(() => {
        if (!controller.signal.aborted) setState({ kind: "error" });
      });
    return () => controller.abort();
  }, [attempt]);

  const data = state.kind === "loaded" ? state.data : undefined;
  return (
    <div className="shell">
      <aside>
        <a href="#inicio" className="brand" aria-label="Traceleaf, início">
          <svg viewBox="0 0 32 32" width="30" height="30" aria-hidden="true">
            <path
              d="M25 5C9 3 3 15 11 23c9 5 17-3 14-18Z"
              fill="currentColor"
            />
            <path d="m8 28 12-16" stroke="#c9dfb0" strokeWidth="2" />
          </svg>
          traceleaf<span className="brand-dot">.</span>
        </a>
        <p className="eyebrow">Seu conhecimento, conectado</p>
        <nav aria-label="Navegação principal">
          <a className="nav-item" href="#inicio" aria-current="page">
            Visão geral <span>↗</span>
          </a>
          <a className="nav-link" href="#proximos-passos">
            Próximos passos
          </a>
        </nav>
        <div className="sidebar-note">
          <span className="dot" /> Desenvolvimento local
          <p>Fundação do projeto · M0</p>
        </div>
      </aside>
      <main id="inicio">
        <header>
          <span>Workspace / Visão geral</span>
          <span className="pill">Prévia de desenvolvimento</span>
        </header>
        <section className="intro">
          <p className="eyebrow">Da informação à atualização</p>
          <h1>Sua base, com contexto.</h1>
          <p>
            Um lugar para manter seus documentos Markdown atualizados, com
            fontes verificáveis e cada mudança sob seu controle.
          </p>
        </section>
        <section className="hero" aria-labelledby="foundation-title">
          <div>
            <span className="step-label">01 / FUNDAÇÃO</span>
            <h2 id="foundation-title">O primeiro passo está aqui.</h2>
            <p>
              A estrutura do Traceleaf está em construção. Esta tela acompanha
              os serviços locais; a biblioteca e os recursos de IA chegam nos
              próximos marcos.
            </p>
          </div>
          <div className="flow" aria-label="Fluxo planejado">
            <span>Fonte</span>
            <b aria-hidden="true">↓</b>
            <span>Contexto + proposta</span>
            <b aria-hidden="true">↓</b>
            <span>Sua revisão</span>
          </div>
        </section>
        <section aria-labelledby="services-title" className="services">
          <div className="section-heading">
            <h2 id="services-title">Ambiente local</h2>
            <button
              onClick={() => setAttempt((n) => n + 1)}
              disabled={state.kind === "loading"}
            >
              Verificar novamente <span aria-hidden="true">↻</span>
            </button>
          </div>
          <div role="status" aria-live="polite">
            {state.kind === "loading" && (
              <p className="notice">Consultando os serviços…</p>
            )}
            {state.kind === "error" && (
              <p className="notice error">
                Não foi possível consultar a API. Confira se os serviços estão
                em execução e tente novamente.
              </p>
            )}
            {data && (
              <>
                <p className="health-summary">
                  {data.readiness.status === "ready"
                    ? "Serviços prontos para desenvolvimento."
                    : "Há serviços indisponíveis. Confira o Docker Compose."}
                </p>
                <div className="cards">
                  {[
                    ["API", true, "FastAPI · Python"],
                    [
                      "PostgreSQL",
                      data.readiness.services.postgresql,
                      "Schema + pgvector",
                    ],
                    [
                      "Redis",
                      data.readiness.services.redis,
                      "Conexão de infraestrutura",
                    ],
                  ].map(([title, ready, detail]) => (
                    <article className="service-card" key={String(title)}>
                      <span
                        className={
                          ready ? "service-state" : "service-state offline"
                        }
                      >
                        {ready ? "Disponível" : "Indisponível"}
                      </span>
                      <h3>{title}</h3>
                      <p>{detail}</p>
                    </article>
                  ))}
                </div>
              </>
            )}
          </div>
        </section>
        <section id="proximos-passos" aria-labelledby="next-title">
          <div className="section-heading">
            <h2 id="next-title">O que vem a seguir</h2>
            <span className="muted">Planejamento da aplicação</span>
          </div>
          <div className="roadmap">
            <article>
              <span className="milestone">M1</span>
              <div>
                <h3>Uma biblioteca que é sua</h3>
                <p>
                  Importar, ler e editar Markdown com histórico. Pastas
                  externas, como Obsidian, serão somente leitura.
                </p>
              </div>
              <span className="tag">Planejado</span>
            </article>
            <article>
              <span className="milestone">M2</span>
              <div>
                <h3>Respostas com evidências</h3>
                <p>
                  Busca híbrida e RAG para encontrar contexto e responder com
                  referências.
                </p>
                {data && (
                  <p className="availability">
                    {data.capabilities.capabilities.rag.reason ===
                    "missing_credentials"
                      ? "IA indisponível: sem credenciais. Integração prevista no M2."
                      : "IA indisponível: integração ainda não implementada."}
                  </p>
                )}
              </div>
              <span className="tag">Planejado</span>
            </article>
            <article>
              <span className="milestone">M3</span>
              <div>
                <h3>Mudanças que você aprova</h3>
                <p>
                  Propostas por documento, comparação de versões e revisão antes
                  de aplicar.
                </p>
              </div>
              <span className="tag">Planejado</span>
            </article>
          </div>
        </section>
        <footer>
          Nenhuma pasta pessoal conectada. Nenhum conteúdo enviado a modelos de
          IA.
        </footer>
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
