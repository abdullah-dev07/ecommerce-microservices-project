SHELL := /bin/bash

PYTHON ?= python3
NPM ?= npm
COMPOSE ?= docker compose

BACKEND_DIR := backend
FRONTEND_DIR := frontend
SERVICES_DIR := $(BACKEND_DIR)/services
COMPOSE_FILE := $(BACKEND_DIR)/docker-compose.yml
COMPOSE_CMD := $(COMPOSE) -f $(COMPOSE_FILE)

SERVICES := user_service product_service order_service
DB_SERVICES := user_db product_db order_db

# Default service for migration targets: make migrate SERVICE=user_service NAME=add_phone
SERVICE ?= user_service
NAME ?= change

.PHONY: help \
	compose-up compose-down compose-logs db-up db-down \
	setup-all setup-user setup-product setup-order \
	init-db-all migrate upgrade downgrade history \
	run-gateway run-user run-product run-order \
	lint format \
	frontend-install frontend-dev frontend-build frontend-lint frontend-typecheck

help:
	@echo "Backend (FastAPI microservices):"
	@echo ""
	@echo "  make compose-up         # start full stack with docker compose"
	@echo "  make compose-down       # stop full stack"
	@echo "  make compose-logs       # tail compose logs"
	@echo "  make db-up              # start only postgres containers"
	@echo "  make db-down            # stop only postgres containers"
	@echo ""
	@echo "  make setup-all          # create .venv + install requirements for all DB services"
	@echo "  make init-db-all        # run aerich init-db once per DB service (first-time bootstrap)"
	@echo "  make migrate SERVICE=user_service NAME=add_phone"
	@echo "  make upgrade SERVICE=user_service"
	@echo "  make downgrade SERVICE=user_service"
	@echo "  make history SERVICE=user_service"
	@echo ""
	@echo "  make run-gateway        # run API gateway locally on :8000"
	@echo "  make run-user           # run user_service locally on :8001"
	@echo "  make run-product        # run product_service locally on :8002"
	@echo "  make run-order          # run order_service locally on :8003"
	@echo ""
	@echo "  make lint               # ruff check (if installed)"
	@echo "  make format             # ruff format (if installed)"
	@echo ""
	@echo "Frontend (Next.js):"
	@echo ""
	@echo "  make frontend-install   # npm install"
	@echo "  make frontend-dev       # next dev (http://localhost:3000)"
	@echo "  make frontend-build     # next build"
	@echo "  make frontend-lint      # next lint"
	@echo "  make frontend-typecheck # tsc --noEmit"

# ─── Backend ──────────────────────────────────────────────────

compose-up:
	$(COMPOSE_CMD) up --build

compose-down:
	$(COMPOSE_CMD) down

compose-logs:
	$(COMPOSE_CMD) logs -f

db-up:
	$(COMPOSE_CMD) up -d $(DB_SERVICES)

db-down:
	$(COMPOSE_CMD) stop $(DB_SERVICES)

setup-user:
	cd $(SERVICES_DIR)/user_service && $(PYTHON) -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

setup-product:
	cd $(SERVICES_DIR)/product_service && $(PYTHON) -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

setup-order:
	cd $(SERVICES_DIR)/order_service && $(PYTHON) -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

setup-all: setup-user setup-product setup-order

init-db-all:
	@echo "Bootstrapping Aerich for all DB services (run once per service)..."
	@for svc in $(SERVICES); do \
		echo "==> $$svc"; \
		cd $(SERVICES_DIR)/$$svc && source .venv/bin/activate && aerich init-db; \
		cd - >/dev/null; \
	done

migrate:
	cd $(SERVICES_DIR)/$(SERVICE) && source .venv/bin/activate && aerich migrate --name $(NAME)

upgrade:
	cd $(SERVICES_DIR)/$(SERVICE) && source .venv/bin/activate && aerich upgrade

downgrade:
	cd $(SERVICES_DIR)/$(SERVICE) && source .venv/bin/activate && aerich downgrade -v 1

history:
	cd $(SERVICES_DIR)/$(SERVICE) && source .venv/bin/activate && aerich history

run-gateway:
	cd $(SERVICES_DIR)/api_gateway && $(PYTHON) -m uvicorn app.main:app --reload --port 8000

run-user:
	cd $(SERVICES_DIR)/user_service && source .venv/bin/activate && uvicorn app.main:app --reload --port 8001

run-product:
	cd $(SERVICES_DIR)/product_service && source .venv/bin/activate && uvicorn app.main:app --reload --port 8002

run-order:
	cd $(SERVICES_DIR)/order_service && source .venv/bin/activate && uvicorn app.main:app --reload --port 8003

lint:
	ruff check $(SERVICES_DIR)

format:
	ruff format $(SERVICES_DIR)

# ─── Frontend ─────────────────────────────────────────────────

frontend-install:
	cd $(FRONTEND_DIR) && $(NPM) install

frontend-dev:
	cd $(FRONTEND_DIR) && $(NPM) run dev

frontend-build:
	cd $(FRONTEND_DIR) && $(NPM) run build

frontend-lint:
	cd $(FRONTEND_DIR) && $(NPM) run lint

frontend-typecheck:
	cd $(FRONTEND_DIR) && $(NPM) run type-check
