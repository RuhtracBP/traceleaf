FROM ghcr.io/astral-sh/uv:0.13.8@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 AS uv
FROM python:3.12.16-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df AS base
COPY --from=uv /uv /uvx /bin/
WORKDIR /app
ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock .python-version alembic.ini ./
COPY apps/api apps/api
COPY packages/core packages/core

FROM base AS test
RUN uv sync --locked --all-packages
COPY tests tests
CMD ["pytest", "-m", "integration", "-v"]

FROM base AS runtime
RUN uv sync --locked --all-packages --no-dev --no-editable \
    && useradd --create-home --uid 10001 traceleaf
USER traceleaf
EXPOSE 8000
CMD ["uvicorn", "traceleaf_api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
