import { afterEach, describe, expect, it, vi } from "vitest";
import { loadOverview } from "./api";

afterEach(() => vi.unstubAllGlobals());

describe("environment status", () => {
  it("preserves a real 503 as unavailable instead of treating it as success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockImplementation((url: string) =>
        Promise.resolve(
          new Response(
            JSON.stringify(
              url.includes("ready")
                ? {
                    status: "unavailable",
                    services: { postgresql: false, redis: true },
                  }
                : { milestone: "M0", capabilities: {} },
            ),
            { status: url.includes("ready") ? 503 : 200 },
          ),
        ),
      ),
    );
    const result = await loadOverview(new AbortController().signal);
    expect(result.readiness.status).toBe("unavailable");
    expect(result.readiness.services.postgresql).toBe(false);
  });

  it("rejects an unexpected HTTP error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("bad gateway", { status: 502 })),
    );
    await expect(loadOverview(new AbortController().signal)).rejects.toThrow(
      "Não foi possível",
    );
  });

  it("does not accept an HTML proxy page as API data", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("<html>Error</html>")),
    );
    await expect(loadOverview(new AbortController().signal)).rejects.toThrow();
  });
});
