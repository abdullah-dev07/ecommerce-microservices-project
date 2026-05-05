# E-Commerce Microservices (FastAPI)

A learning-focused microservices project: 3 independent services + 1 API Gateway,
each with its own PostgreSQL database, communicating over HTTP.

---

## Architecture

```
                 Client
                   │
                   ▼
          ┌─────────────────┐
          │   API Gateway   │  :8000 — only exposed port
          └────────┬────────┘
                   │ HTTP
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │  User  │ │Product │ │ Order  │
   │  Svc   │ │  Svc   │ │  Svc   │
   │ :8001  │ │ :8002  │ │ :8003  │
   └────┬───┘ └───┬────┘ └───┬────┘
        │         │          │
        ▼         ▼          ▼
   [user_db] [product_db] [order_db]
    :5433      :5434       :5435
```

The Order Service calls the User and Product services over HTTP to validate
data and reserve stock. Services are decoupled but cooperate.

---

## Project structure

```
ecommerce-microservice-arc/
├── docker-compose.yml
├── .env.example
└── services/
    ├── api_gateway/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app/
    │       ├── main.py                    # FastAPI() + include_router
    │       ├── core/
    │       │   ├── config.py              # pydantic-settings
    │       │   └── http_client.py         # shared AsyncClient + proxy()
    │       ├── schemas/                   # request bodies validated at the edge
    │       └── api/routes/                # health, users, products, orders
    ├── user_service/
    │   └── app/
    │       ├── main.py
    │       ├── core/        (config, security)
    │       ├── db/          (base, session)
    │       ├── models/      (SQLAlchemy)
    │       ├── schemas/     (Pydantic)
    │       ├── services/    (business logic)
    │       └── api/         (deps + routes)
    ├── product_service/                   # same layout
    └── order_service/                     # same layout + clients/
        └── app/
            ├── clients/
            │   ├── user_client.py         # outbound httpx → user_service
            │   └── product_client.py      # outbound httpx → product_service
            └── ...
```

### Why this layout

| Layer | Purpose | Knows about |
|---|---|---|
| `api/routes/` | HTTP shape: paths, status codes, request/response models | FastAPI |
| `services/` | Business rules ("create order = verify user, check stock, persist") | DB + clients |
| `clients/` | Outbound calls to other microservices (timeouts, retries, error mapping) | `httpx` |
| `models/` | SQLAlchemy ORM | DB only |
| `schemas/` | Pydantic for I/O validation | nothing |
| `core/config.py` | Single typed source of env vars | `pydantic-settings` |

---

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

All services start automatically with isolated databases. Only the gateway
publishes a port (`:8000`). Open the interactive docs at
[http://localhost:8000/docs](http://localhost:8000/docs).

---

## API reference (via the Gateway)

### Health
```
GET    /health                   → gateway + downstream service status
```

### Users
```
POST   /users                    → create user
GET    /users/{id}               → get user
GET    /users                    → list users
```

### Products
```
POST   /products                 → create product
GET    /products/{id}            → get product
GET    /products                 → list products
```

### Orders
```
POST   /orders                   → create order (verifies user + stock, deducts stock)
GET    /orders/{id}              → get order
GET    /users/{id}/orders        → list orders for a user
PATCH  /orders/{id}/cancel       → cancel order (restores stock)
GET    /orders/{id}/detail       → aggregated: order + customer
```

---

## Test flow (curl)

```bash
BASE=http://localhost:8000

# 1. Create a user
curl -X POST $BASE/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com", "password": "supersecret123"}'

# 2. Create a product
curl -X POST $BASE/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "Fast laptop", "price": 999.99, "stock": 10}'

# 3. Place an order
curl -X POST $BASE/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "items": [{"product_id": 1, "quantity": 2}]}'

# 4. Aggregated detail
curl $BASE/orders/1/detail

# 5. Cancel — stock is restored
curl -X PATCH $BASE/orders/1/cancel
```

---

## Key learning points

| Concept | Where to look |
|---|---|
| One DB per service | `docker-compose.yml` |
| Inter-service HTTP | `services/order_service/app/clients/` |
| Lifespan-managed shared `AsyncClient` | `services/*/app/core/http_client.py` |
| API Gateway proxying | `services/api_gateway/app/core/http_client.py` (`proxy()`) |
| Aggregation at the edge | `services/api_gateway/app/api/routes/orders.py` (`/orders/{id}/detail`) |
| Saga-style compensation | `services/order_service/app/services/order_service.py` (`_restore_stock`) |
| Password hashing (bcrypt) | `services/user_service/app/core/security.py` |
| Typed config (`pydantic-settings`) | `services/*/app/core/config.py` |

---

## Running a single service locally (without Docker)

```bash
cd services/user_service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:password@localhost:5433/user_db
uvicorn app.main:app --reload --port 8001
```

---

## Suggested next steps

1. **Alembic migrations** — replace `Base.metadata.create_all` with versioned migrations.
2. **Auth at the gateway** — issue JWTs from `user_service`, validate at the gateway,
   forward identity as `X-User-Id` to downstream services.
3. **Resilience** — add retries (`tenacity`) and circuit breakers (`pybreaker`)
   to the inter-service clients.
4. **Observability** — structured logging + OpenTelemetry tracing across services.
5. **Async messaging** — emit an `OrderCreated` event for emails / analytics
   instead of doing everything synchronously in the request path.
6. **Conditional stock UPDATE** — replace the read-modify-write in
   `product_service.update_stock` with a single conditional `UPDATE` to avoid
   races under concurrency.
