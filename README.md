# TicTacToe – Backend

FastAPI-basiertes REST-Backend für ein Multiplayer-TicTacToe-Spiel. Die gesamte Spiellogik (Gewinnprüfung, Zugreihenfolge, Statusverwaltung) liegt hier im Backend.

---

## Technologie-Stack

| Technologie | Verwendung |
|---|---|
| Python 3.11 | Programmiersprache |
| FastAPI | Web-Framework |
| SQLAlchemy (async) | ORM / Datenbankzugriff |
| PostgreSQL + asyncpg | Datenbank |
| Pydantic | Schema-Validierung |

---

## Projektstruktur

```
app/
├── api/
│   ├── routes/
│   │   ├── games.py        # Alle Spiel-Endpunkte
│   │   └── users.py
│   └── router.py
├── core/
│   ├── config.py           # Settings (DATABASE_URL, API_KEYS)
│   ├── dependencies.py     # User-Auflösung per API-Key
│   └── security.py         # API-Key Validierung
├── db/
│   ├── base.py
│   └── session.py
├── models/
│   ├── game.py             # SQLAlchemy Game-Modell
│   └── user.py
├── schemas/
│   ├── game.py             # Pydantic Schemas (GameOut, Move, ...)
│   └── users.py
├── services/
│   └── tictactoe.py        # Spiellogik (Gewinnprüfung, Züge)
└── main.py
```

---

## API Endpunkte

| Methode | Pfad | Beschreibung |
|---|---|---|
| `POST` | `/games` | Neues Spiel erstellen (als Player X) |
| `GET` | `/games` | Alle eigenen Spiele auflisten |
| `GET` | `/games/{id}` | Einzelnes Spiel abrufen |
| `POST` | `/games/{id}/join` | Spiel als Player O beitreten |
| `PUT` | `/games/{id}/move/{pos}` | Zug machen (Position 1–9) |
| `DELETE` | `/games/{id}` | Abgeschlossenes Spiel löschen |

---

## Konfiguration

Erstelle eine `.env` Datei im Verzeichnis `tic.tac.toe/`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/tictactoe
API_KEYS=alice:alice-key,bob:bob-key
API_KEY_HEADER=X-API-Key
```

**`DATABASE_URL`** – Verbindungsstring zur PostgreSQL-Datenbank.  
**`API_KEYS`** – Format `username:apikey`, mehrere Einträge kommagetrennt. Benutzer werden beim ersten Request automatisch in der Datenbank angelegt.  
**`API_KEY_HEADER`** – Name des Headers (Standard: `X-API-Key`).

---

## Starten

```bash
cd C:\Schule\INSY\FastAPI_TicTacToe\tic.tac.toe

# Abhängigkeiten installieren (einmalig)
pip install -r requirements.txt

# .env Datei anlegen (siehe oben)

# Server starten
uvicorn app.main:app --reload
```

Backend läuft unter: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

---

## Authentifizierung

Alle Endpunkte sind per API-Key geschützt. Der Key wird im Header mitgeschickt:

```
X-API-Key: alice-key
```

Der zugehörige Username wird aus der `.env` aufgelöst. Existiert der User noch nicht in der Datenbank, wird er automatisch angelegt.