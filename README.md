# Booking Backend (FastAPI)

## Quick start (dev)

1. Copy `.env.example` to `.env` and configure DB/Redis URLs and STRIPE keys.
2. `docker-compose up --build` (will run Postgres + Redis + app)
3. Run migrations: `docker-compose exec web alembic upgrade head`
4. Open `http://localhost:8000/docs` for interactive OpenAPI.

## Features
- JWT auth (access + refresh)
- Resource CRUD
- Booking create w/atomic overlap prevention (Postgres exclusion constraint)
- Advisory lock fallback for compatibility
- Stripe webhook handler stub
- Background tasks for pending expiration & emails
- Docker Compose for dev
