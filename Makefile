.PHONY: help setup lint fmt typecheck test check dev-web

help: ## list targets
	@grep -E '^[a-z-]+:.*## ' Makefile | awk -F ':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'

setup: ## install locked backend and web dependencies
	cd backend && uv sync --frozen
	cd web && npm ci

lint: ## lint and check formatting (backend)
	cd backend && uv run --frozen ruff check .
	cd backend && uv run --frozen ruff format --check .

fmt: ## format the backend code
	cd backend && uv run --frozen ruff format .
	cd backend && uv run --frozen ruff check --fix .

typecheck: ## strict type checks, backend and web
	cd backend && uv run --frozen mypy
	cd web && npm run --silent typecheck

test: ## run backend and web tests
	cd backend && uv run --frozen pytest
	cd web && npm test --silent

check: lint typecheck test ## everything

dev-web: ## run the web app on :5173
	cd web && npm run dev
