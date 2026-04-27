# TicTacToe FastAPI

Two-player TicTacToe REST API using FastAPI, async SQLAlchemy, and PostgreSQL.

## Key decisions

- Auth uses pre-shared API keys via `X-API-Key`.
- Owner is `X`, second player joins as `O` via `POST /games/{game_id}/join`.
- Board is a 9-char string using `.` for empty cells.
- Game status values: `IN_PROGRESS`, `X_WON`, `O_WON`, `DRAW`.

## Setup

### Option A: Docker (recommended)

1) Start the API + database:

```bash
docker compose up --build
```

2) The API will be available at:

```text
http://localhost:8000
```

3) pgAdmin will be available at:

```text
http://localhost:5050
```

Login with the credentials from `.env`.

### Option B: Local venv

Removed. This project is Docker-only.

## API usage (example flow)

1) Create a game (owner becomes `X`):

```bash
curl -X POST http://localhost:8000/games \
  -H "X-API-Key: alice-key"
```

2) Join game as `O`:

```bash
curl -X POST http://localhost:8000/games/{game_id}/join \
  -H "X-API-Key: bob-key"
```

3) Make a move:

```bash
curl -X PUT http://localhost:8000/games/{game_id}/move/1 \
  -H "X-API-Key: alice-key"
```

4) List games for current user:

```bash
curl http://localhost:8000/games \
  -H "X-API-Key: alice-key"
```

## Testing

Set `DATABASE_URL` and `API_KEYS` to a test database, then run:

```bash
pytest
```

## Endpoint summary

- `POST /games` create a game (owner is `X`)
- `POST /games/{game_id}/join` join as `O`
- `GET /games` list games for current user
- `GET /games/{game_id}` get game details
- `PUT /games/{game_id}/move/{position}` apply a move
- `DELETE /games/{game_id}` delete a completed game
