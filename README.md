# Alfa Focus Knowledge Assistant

An internal, citation-first knowledge assistant for **Alfa Focus**, a specialist SMSF administration practice in South Melbourne. Built as the RMIT COSC2408 Programming Project 1 capstone.

The problem: Australian superannuation rules change constantly - 1 July 2026 alone brought Division 296, payday super, and an indexed transfer balance cap - and firm-specific procedure lives in senior heads rather than in writing. Accountants lose time re-deriving answers, and two staff can give a referring planner two different answers.

The assistant answers two kinds of question and keeps them strictly separate:

- **What does the law require?** Grounded in ATO guidance, rulings, legislation, TPB and APESB, cited to a source you can open.
- **How does Alfa Focus do this?** Grounded in the firm's own procedures, labelled as firm convention rather than law.

Every answer carries resolvable citations and an explicit income year. It assists a registered tax agent; it never signs off.

> **Status: pre-client-meeting.** The client has not been met. Everything in [`docs/CLIENT-BRIEF.md`](docs/CLIENT-BRIEF.md) is open-source research carrying explicit confidence markers. Do not quote a `MEDIUM` or `LOW` fact to the client as settled.

## Documentation

Read in this order. Each is written to be read on its own, but the design decisions only make sense after the domain primer.

| Doc | What it answers |
|---|---|
| [`docs/CLIENT-BRIEF.md`](docs/CLIENT-BRIEF.md) | Who Alfa Focus actually is. **They are an SMSF specialist, not a general tax consultancy** - read this before assuming scope |
| [`docs/DOMAIN-PRIMER.md`](docs/DOMAIN-PRIMER.md) | Australian SMSF practice for a team with no accounting background; what is changing in 2026; the professional-obligation constraints that drive the architecture |
| [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) | Numbered, testable requirements: chatbot behaviour, file upload, data handling, edge cases. What the build is held to |
| [`docs/RAG-DESIGN.md`](docs/RAG-DESIGN.md) | The two-corpus split, the chunk schema, hybrid + temporal retrieval, and **which file in this repo owns each piece** |
| [`docs/PROMPTS.md`](docs/PROMPTS.md) | The system prompt, refusal templates, query-understanding prompt. Source of truth for `app/rag/generator.py` |
| [`docs/EVALUATION.md`](docs/EVALUATION.md) | Benchmark taxonomy, 28 seed questions, metrics and gates, LLM-judge design, what `/testing` must do |
| [`docs/CLIENT-MEETING-QUESTIONS.md`](docs/CLIENT-MEETING-QUESTIONS.md) | The 14 questions that change the build, ranked |
| [`docs/GIT-WORKFLOW.md`](docs/GIT-WORKFLOW.md) | Branch naming, commit format, PR and CI requirements |

## Design principles

These are enforced in code and checked by the evaluation suite, not aspirational:

1. **No citation, no claim.** If retrieval finds nothing, the assistant escalates rather than guesses. A confident unsourced answer is the worst possible output for a regulated client.
2. **Every volatile claim is scoped to an income year.** Undated tax advice is wrong advice.
3. **Law and firm practice are never blended in one sentence.** Separate labelled sections, attributed per claim.
4. **No client identifiers, no member-specific figures.** The assistant answers rules questions. Client data stays out by construction.
5. **Deterministic checks beat judged ones.** Citation resolution is a lookup and an HTTP check, gated at 100% with no exceptions.

## Project structure

```
accounting-knowledge-assistant/
├── app/
│ ├── main.py               # Entry point — registers routes, mounts Chainlit at /chat (mounted LAST)
│ ├── config.py             # Loads all env vars from one place (.env locally, Render env vars in prod)
│ │
│ ├── routes/
│ │ ├── upload.py           # /upload — document ingest into the corpus
│ │ └── testing.py          # /testing — benchmark runner and evaluation results
│ │
│ ├── chainlit/
│ │ └── chainlit_app.py     # Chat app: on_chat_start, on_message, auth callback
│ │
│ ├── services/
│ │ ├── document_service.py # Document lifecycle, parsing, structure-aware chunking, metadata
│ │ └── storage_service.py  # Supabase Storage: upload/fetch raw files
│ │
│ ├── rag/
│ │ ├── embedder.py         # Text → vector embeddings
│ │ ├── retriever.py        # Hybrid search + temporal filter + corpus routing + rerank
│ │ └── generator.py        # Prompt assembly + LLM call + citation validation
│ │
│ └── db/
│   ├── database.py         # SQLAlchemy session setup and establishes connection
│   ├── models.py           # ORM models: Document, DocumentChunk, AppUser, EvalResult
│   └── schema.sql          # Table definitions — mirrors models.py
│
├── benchmarks/
│   └── questions.jsonl     # Versioned benchmark set — see docs/EVALUATION.md
│
├── templates/              # Jinja2 templates for /upload and /testing
├── static/                 # Shared CSS and minimal client-side JS
├── docs/                   # See the documentation table above
│
├── .env.example            # Documents every required env var, no real values
├── Dockerfile
├── requirements.txt        # Pinned to versions Chainlit actually supports
└── README.md
```

### Layer overview

- **`routes/`** — HTTP handlers. Each route renders a template or delegates to `services/`/`rag/` — no business logic lives here directly.
- **`chainlit/`** — the chat interface. `on_message` is where a user's question enters the RAG pipeline via `rag/`.
- **`services/`** — logic that isn't HTTP- or chat-specific: document lifecycle and file storage. Keeps `routes/` from growing bloated handlers.
- **`rag/`** — the pipeline itself, split by responsibility (embed → retrieve → generate) so each piece can be tested and swapped independently. `retriever.py` is the highest-value file in the repo: retrieval, not generation, is where RAG systems actually fail.
- **`db/`** — the persistence layer. `models.py` and `schema.sql` mirror each other — update both if the schema changes. The proposed schema is in [`docs/RAG-DESIGN.md`](docs/RAG-DESIGN.md) section 4.

### Database

Postgres + pgvector via Supabase, provisioned separately from Render so data persists independently of the app container. Two Supabase projects — one dev, one prod — matching the free tier's two-project allowance. `DATABASE_URL` in `.env` (dev) or Render's dashboard (prod) determines which one the app talks to.

pgvector was the right call for this domain specifically: one query can filter on effective dates, match exact statutory identifiers via a generated `tsvector`, and rank by vector distance — no second search system to run.

## Run mounted FastAPI + Chainlit app

### First Time
MacOS/Linux
```bash
python3.13.9 -m venv .venv
pip install -r requirements.txt
```

### To Start
Chainlit is mounted into the FastAPI app (see `app/main.py`), so the chat UI is available under `/chat` on the FastAPI server. From the repository root:

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

## Contributing

`main` is protected. Branch, PR, squash merge — see [`docs/GIT-WORKFLOW.md`](docs/GIT-WORKFLOW.md) for the enforced branch and commit naming rules.

Two additional rules for this project:

- **A prompt change is a behaviour change.** Edit [`docs/PROMPTS.md`](docs/PROMPTS.md) and `generator.py` in the same PR, re-run the benchmark, and put the before/after per-class scores in the PR description.
- **A schema change touches two files.** `models.py` and `schema.sql` must stay mirrored.

## Known gaps in the scaffold

Tracked here so nobody assumes they work:

- `Dockerfile` is empty — Render deployment cannot succeed until it is written, and no CI check catches this.
- `.github/workflows/deploy.yml` does not deploy. It contains a commit-message check. Rename it to `commit-message.yml` or make it deploy.
- `app/db/models.py` and `app/db/schema.sql` are empty — proposed contents in [`docs/RAG-DESIGN.md`](docs/RAG-DESIGN.md) section 4.
- `mlflow` is not in `requirements.txt`; the evaluation design in [`docs/EVALUATION.md`](docs/EVALUATION.md) assumes it.
- `ci.yml` has a commented-out `pytest` step — that is where the evaluation gates hook in.
