import { expect, test } from "@playwright/test";

test("a dependency outage is shown as unavailable", async ({ page }) => {
  await page.route("**/api/v1/health/ready", (route) =>
    route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({
        status: "unavailable",
        services: { postgresql: false, redis: true },
      }),
    }),
  );
  await page.goto("/");
  await expect(
    page.getByText("Há serviços indisponíveis.", { exact: false }),
  ).toBeVisible();
  const database = page
    .getByRole("article")
    .filter({ has: page.getByRole("heading", { name: "PostgreSQL" }) });
  await expect(
    database.getByText("Indisponível", { exact: true }),
  ).toBeVisible();
});

test("real stack is ready and planned AI features stay unavailable", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Sua base, com contexto." }),
  ).toBeVisible();
  await expect(
    page.getByText("Serviços prontos para desenvolvimento."),
  ).toBeVisible();
  await expect(
    page.getByText("IA indisponível: sem credenciais.", { exact: false }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Verificar novamente" }).click();
  await expect(
    page.getByText("Serviços prontos para desenvolvimento."),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});

test("API failure can be retried without reloading the page", async ({
  page,
}) => {
  await page.route("**/api/v1/**", (route) => route.abort());
  await page.goto("/");
  await expect(
    page.getByText("Não foi possível consultar a API.", { exact: false }),
  ).toBeVisible();
  await page.unroute("**/api/v1/**");
  await page.getByRole("button", { name: "Verificar novamente" }).click();
  await expect(
    page.getByText("Serviços prontos para desenvolvimento."),
  ).toBeVisible();
});
