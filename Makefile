.PHONY: setup up down check integration e2e

setup:
	python3 scripts/setup_env.py
	uv sync --locked --all-packages
	pnpm install --frozen-lockfile

up:
	docker compose up --build --wait

down:
	docker compose down

check:
	uv run --locked ruff check .
	uv run --locked ruff format --check .
	uv run --locked mypy
	uv run --locked pytest -m 'not integration'
	pnpm format:check
	pnpm typecheck
	pnpm test
	pnpm build

integration:
	python3 scripts/check_integration.py

e2e:
	pnpm test:e2e
