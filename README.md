## Project Structure
```
alfafocus-pilot/
├── app/
│ ├── main.py               # Entry point — registers routes, mounts Chainlit at /chat (mounted LAST)
│ ├── config.py             # Loads all env vars from one place (.env locally, Render env vars in prod)
│ │
│ ├── routes/
│ │ ├── upload.py           # /upload — document upload page
│ │ └── testing.py          # /testing — LLM testing/evaluation page
│ │
│ ├── chainlit/
│ │ └── chainlit_app.py     # Chat app: on_chat_start, on_message, auth callback
│ │
│ ├── services/
│ │ ├── document_service.py # Document lifecycle: create record, update status
│ │ └── storage_service.py  # Supabase Storage: upload/fetch raw files
│ │
│ ├── rag/
│ │ ├── embedder.py         # Text → vector embeddings 
│ │ ├── retriever.py        # Top-k similarity search against document_chunks
│ │ └── generator.py        # Prompt assembly + LLM call 
│ │
│ └── db/
│   ├── database.py         # SQLAlchemy session setup and establishes connection
│   ├── models.py           # ORM models: Document, DocumentChunk, AppUser, EvalResult (defining the data)
│   └── schema.sql          # Help create the tables in the database
│
├── templates/
│   ├── upload.html         # Jinja2 template for /upload
│   └── testing.html        # Jinja2 template for /testing
│
├── static/
│    ├── css/style.css       # Shared styling for the two custom pages
│    └── js/main.js          # Client-side JS (minimal — no functionality until it's needed)
│
├── .env.example            # Documents every required env var, no real values
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt        # Pinned to versions Chainlit actually supports
└── README.md
```

### Layer overview

- **`routes/`** — thin HTTP handlers. Each route renders a template or delegates to `services/`/`rag/` — no business logic lives here directly.
- **`chainlit/`** — the chat interface. `on_message` is where a user's question enters the RAG pipeline via `rag/`.
- **`services/`** — logic that isn't HTTP- or chat-specific: document lifecycle and file storage. Keeps `routes/` from growing bloated handlers.
- **`rag/`** — the retrieval-augmented generation pipeline itself, split by responsibility (embed → retrieve → generate) so each piece can be tested and swapped independently.
- **`db/`** — the persistence layer: ORM models, schema, and connection setup. `models.py` and `schema.sql` mirror each other — update both if the schema changes.

### Database

Postgres + pgvector via Supabase, provisioned separately from Render so data persists independently of the app container. Two Supabase projects — one dev, one prod — matching the free tier's two-project allowance. `DATABASE_URL` in `.env` (dev) or Render's dashboard (prod) determines which one the app talks to.

## Run mounted FastAPI + Chainlit app

If you mounted Chainlit into the FastAPI app (see `app/main.py`) the chat UI is available under `/chat` on the FastAPI server. From the repository root run one of these:

- Local only (recommended for development):

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Expose on LAN (other devices on same network can reach it):

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open the chat UI at:

```text
http://localhost:8000/chat        # local-only
http://<your-machine-ip>:8000/chat # from another device on LAN
```

Notes:
- If you run Uvicorn from inside the `app/` folder instead, the module path becomes `main:app` (example: `cd app && uvicorn main:app --reload`).
- If `uvicorn` isn't on your PATH use the venv binary: `./.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
- For production, run Uvicorn behind a reverse proxy (nginx) or use a process manager; avoid running as root on privileged ports.

