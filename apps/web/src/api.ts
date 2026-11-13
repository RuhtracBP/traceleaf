export interface Readiness {
  status: "ready" | "unavailable";
  services: { postgresql: boolean; redis: boolean };
}

export interface Capabilities {
  milestone: "M0";
  capabilities: Record<
    "markdown" | "text_search" | "rag" | "proposals",
    {
      available: boolean;
      reason: "not_implemented" | "missing_credentials";
      milestone: string;
    }
  >;
}

async function getJson<T>(
  path: string,
  signal: AbortSignal,
  acceptUnavailable = false,
): Promise<T> {
  const response = await fetch(`/api/v1/${path}`, {
    signal: AbortSignal.any([signal, AbortSignal.timeout(10_000)]),
  });
  if (!response.ok && !(acceptUnavailable && response.status === 503)) {
    throw new Error(
      "Não foi possível consultar a API. Confira se os serviços estão em execução.",
    );
  }
  return response.json() as Promise<T>;
}

export async function loadOverview(signal: AbortSignal) {
  const [readiness, capabilities] = await Promise.all([
    getJson<Readiness>("health/ready", signal, true),
    getJson<Capabilities>("capabilities", signal),
  ]);
  return { readiness, capabilities };
}
