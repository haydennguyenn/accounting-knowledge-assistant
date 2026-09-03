# Database Architecture: PostgreSQL + pgvector + BGE-M3

This document explains the database architecture, vector embedding strategy, and how PostgreSQL with pgvector powers the RAG retrieval pipeline.

## Overview

The knowledge assistant uses **PostgreSQL with pgvector** hosted on **Supabase** for persistent storage and vector similarity search. Documents are chunked, embedded using **BAAI/bge-m3**, and stored as 1024-dimensional vectors alongside their text content.

### Why PostgreSQL + pgvector?

For Australian SMSF practice, one query must:
- Filter by effective dates (e.g., "rules active in 2025-26 income year")
- Match exact statutory identifiers (e.g., "Div 296", "ITAA 1997 s 292-85")
- Rank by semantic similarity

pgvector allows all three operations in a single SQL query with HNSW or IVFFlat indexing. The alternative — Pinecone or Weaviate for vectors, Postgres for metadata, full-text search in Elasticsearch — means three systems to sync and three round trips per query.

| Environment | Purpose | Connection |
|-------------|---------|------------|
| **Dev** | Local development, seeded with test documents | `SUPABASE_DB_URL` in `.env` |

Both use Supabase's free tier (500MB storage, 2GB bandwidth/month). Data persists independently of the Render container.

---

## Schema

Defined in two mirrored locations (update both):
- `app/db/schema.sql` — SQL DDL for Supabase SQL editor
- `app/db/models.py` — SQLAlchemy ORM models for Python app

### Core Tables

#### `documents`
Tracks uploaded files and their processing status.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `filename` | text | Original filename (e.g., `"TR 2024-1.pdf"`) |
| `source_label` | text | Corpus identifier: `"law"` or `"firm"` |
| `storage_path` | text | Supabase Storage path to raw file |
| `status` | text | `"pending"` → `"ready"` → `"failed"` |
| `uploaded_by` | text | Email of uploader (from Chainlit auth) |
| `uploaded_at` | timestamp | Upload timestamp |

#### `document_chunks`
Stores text chunks and their vector embeddings. This is the table queried during retrieval.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `document_id` | integer | FK → `documents.id` (cascade delete) |
| `chunk_index` | integer | 0-based chunk position in document |
| `content` | text | Raw text content (512-token chunks) |
| `embedding` | vector(1024) | BGE-M3 embedding |

**Constraints:**
- `unique(document_id, chunk_index)` — prevents duplicate chunks on re-ingestion

**Indexes:**
```sql
create index document_chunks_embedding_idx
  on document_chunks using ivfflat (embedding vector_cosine_ops);
```

IVFFlat index accelerates cosine similarity search once the table has substantial data. For <10k chunks, pgvector uses exact search (no index needed).

#### `app_users`
Stores authenticated users (Chainlit OAuth).

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `email` | text | Unique email |
| `role` | text | `"staff"` or `"admin"` |
| `created_at` | timestamp | Account creation |

#### `eval_results`
Stores benchmark results from `/testing` endpoint.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `question` | text | Benchmark question |
| `expected_answer` | text | Ground truth (if available) |
| `model_name` | text | LLM used (e.g., `"gemini-2.5-flash"`) |
| `model_answer` | text | Generated answer |
| `accuracy_score` | integer | 0-100 quality score |
| `latency_ms` | integer | Response time |
| `cost_usd` | integer | Inference cost in microdollars |
| `created_at` | timestamp | Evaluation timestamp |

---

## Vector Embeddings with BGE-M3

### Model: BAAI/bge-m3

**BGE-M3** is a multilingual dense retriever from the Beijing Academy of Artificial Intelligence, trained on 700M+ text pairs. It produces 1024-dimensional embeddings optimized for semantic search.

- **Hugging Face**: `BAAI/bge-m3`
- **Output dimension**: 1024
- **Max input tokens**: 8192 (we chunk at 512 for granular retrieval)
- **Normalization**: L2-normalized by default (cosine similarity = dot product)

### Why BGE-M3?

| Criterion | BGE-M3 | Alternatives |
|-----------|--------|--------------|
| **Domain fit** | Trained on academic/technical text, strong on statutory language | OpenAI `text-embedding-3-large` optimized for general web text |
| **Cost** | Free (self-hosted via Hugging Face Inference API) | OpenAI charges $0.13/1M tokens |
| **Latency** | ~200ms per chunk batch (HF serverless) | ~150ms (OpenAI) |
| **Dimensionality** | 1024 (fits IVFFlat index) | 3072 (OpenAI large) — 3× storage |

For a regulated domain with technical jargon (SMSF, SIS Act, CGT), a model trained on formal documents outperforms web-trained embedders.

### Embedding Pipeline

Located in `app/rag/embedder.py` (currently empty — implementation pending).

**Expected flow:**
1. Receive chunked text from `app/services/document_service.py`
2. Call Hugging Face Inference API with `BAAI/bge-m3` model
3. Batch chunks (max 32 per request) to reduce round trips
4. Store 1024-dimensional vectors in `document_chunks.embedding`

**Configuration:**
```python
# app/config.py
HF_TOKEN: str = os.getenv("HF_TOKEN", "")
```

Get your token from https://huggingface.co/settings/tokens and add to `.env`:
```bash
HF_TOKEN=hf_your_token_here
```

### Cosine Similarity Search

pgvector's `vector_cosine_ops` computes cosine similarity between query embedding and stored chunk embeddings:

```sql
SELECT content, 1 - (embedding <=> query_vector) AS similarity
FROM document_chunks
ORDER BY embedding <=> query_vector
LIMIT 10;
```

The `<=>` operator is cosine distance (0 = identical, 2 = opposite). Subtract from 1 to get similarity (1 = identical, -1 = opposite).

---

## Connection Setup

### Local Development

1. **Create Supabase project** at https://supabase.com
2. **Enable pgvector extension** in SQL editor:
   ```sql
   create extension if not exists vector;
   ```
3. **Run schema** from `app/db/schema.sql`
4. **Get connection string** from Project Settings → Database:
   ```
   postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
   ```
5. **Add to `.env`**:
   ```bash
   SUPABASE_DB_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
   ```

### Testing Connection

Run the database test script:

```bash
# From project root
python -m tests.db.test_connection
```

Expected output:
```
✓ Connected to PostgreSQL
✓ pgvector extension installed
✓ Tables exist: documents, document_chunks, app_users, eval_results
```

---

## SQLAlchemy Integration

Located in `app/db/database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(settings.SUPABASE_DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**`pool_pre_ping=True`** ensures the connection pool detects stale connections (important for Supabase's serverless architecture).

### ORM Models

Defined in `app/db/models.py` using SQLAlchemy 2.0 syntax:

```python
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

EMBEDDING_DIM = 1024  # BGE-M3 output dimension

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(EMBEDDING_DIM), nullable=False)
    
    document = relationship("Document", back_populates="chunks")
```

**Key detail:** `Vector(1024)` is from the `pgvector` Python library. Install via:
```bash
pip install pgvector
```

---

## Retrieval Query Pattern

Located in `app/rag/retriever.py` (implementation pending).

**Expected hybrid retrieval:**

1. **Embed query** with BGE-M3
2. **Vector search** for top 20 candidates:
   ```sql
   SELECT id, content, 1 - (embedding <=> :query_embedding) AS score
   FROM document_chunks
   ORDER BY embedding <=> :query_embedding
   LIMIT 20;
   ```
3. **Rerank** by recency (if query mentions income year) or exact keyword match
4. **Return top 5** to generator

This two-stage approach (recall → rerank) is standard for RAG systems. The vector index retrieves broadly; the reranking stage applies domain-specific filters.

---

## Storage Costs

Supabase free tier: **500MB database + 1GB file storage**.

**Per-document storage:**
- Raw PDF: ~200KB
- 100 chunks × (512 tokens text + 1024-dim vector): ~150KB
- Total: ~350KB per document

**Capacity:** ~1,400 documents before hitting free tier limit. Upgrade to Pro ($25/mo) for 8GB.

---

## Migration Notes

### If Switching from Pinecone

1. Export vectors from Pinecone
2. Bulk insert into `document_chunks` with `COPY` command (faster than ORM):
   ```bash
   psql $SUPABASE_DB_URL -c "\COPY document_chunks(document_id, chunk_index, content, embedding) FROM 'vectors.csv' CSV"
   ```
3. Build IVFFlat index after bulk load

### If Changing Embedding Model

If switching from BGE-M3 (1024-dim) to another model:

1. Update `EMBEDDING_DIM` in `app/db/models.py`
2. Alter table:
   ```sql
   ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(new_dim);
   ```
3. Drop and recreate index:
   ```sql
   DROP INDEX document_chunks_embedding_idx;
   CREATE INDEX document_chunks_embedding_idx ON document_chunks USING ivfflat (embedding vector_cosine_ops);
   ```
4. Re-embed all documents (use `app/services/document_service.py` with `force_reembed=True`)

---

## Performance Tuning

### Index Choice

| Index Type | Build Time | Query Speed | Memory | When to Use |
|------------|------------|-------------|--------|-------------|
| **IVFFlat** | Fast | Good | Low | <1M vectors, exact recall not critical |
| **HNSW** | Slow | Excellent | High | >1M vectors, low-latency requirements |

For this project, IVFFlat is appropriate. Switch to HNSW if query latency exceeds 200ms with >100k chunks.

### Query Optimization

pgvector scans vectors linearly until index threshold (default: 1000 rows). With <1000 chunks, no index is used — this is expected and fast enough (<50ms).

To force index usage even with small tables:
```sql
SET ivfflat.probes = 10;  -- Higher = more accurate, slower
```

---

## Security

1. **Never commit `SUPABASE_DB_URL`** — it contains the database password. Keep it in `.env` (gitignored) or Render env vars.
2. **Rotate Supabase passwords** if leaked. Regenerate from Project Settings → Database.
3. **Enable Row-Level Security (RLS)** on Supabase tables if exposing via PostgREST API (not applicable for this app — direct SQLAlchemy access only).
4. **Restrict IP access** in Supabase dashboard if using static IP (Render doesn't provide this on free tier).

---

## Troubleshooting

### "No module named 'pgvector'"
```bash
pip install pgvector
```

### "Extension 'vector' does not exist"
Run in Supabase SQL editor:
```sql
CREATE EXTENSION vector;
```

### "Connection refused" or timeout
- Check `SUPABASE_DB_URL` in `.env` matches Supabase dashboard
- Verify network connectivity: `psql $SUPABASE_DB_URL -c "SELECT 1;"`
- Supabase pauses inactive projects after 7 days — wake it by visiting the dashboard

### Slow vector search (>500ms)
- Check index exists: `\d document_chunks` in psql
- Rebuild index if stale: `REINDEX INDEX document_chunks_embedding_idx;`
- Profile query: `EXPLAIN ANALYZE SELECT ...`

---

## References

- [pgvector GitHub](https://github.com/pgvector/pgvector) — installation, indexing strategies, performance tuning
- [Supabase pgvector Guide](https://supabase.com/docs/guides/ai/vector-columns) — setup and best practices
- [BGE-M3 Model Card](https://huggingface.co/BAAI/bge-m3) — architecture, training data, benchmarks
- [Hugging Face Inference API](https://huggingface.co/docs/api-inference/index) — serverless embedding endpoint
