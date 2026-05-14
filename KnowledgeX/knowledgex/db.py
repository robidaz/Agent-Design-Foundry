"""psycopg connection + DDL bootstrap for the kb_chunks table.

DDL matches Appendix A of the design spec. Idempotent: safe to call on every
ingestion run.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import psycopg
from pgvector.psycopg import register_vector

from knowledgex.config import load_env

EXT_DDL = "CREATE EXTENSION IF NOT EXISTS vector;"

TABLE_DDL = """
CREATE TABLE IF NOT EXISTS kb_chunks (
    chunk_id        TEXT PRIMARY KEY,
    source_doc      TEXT NOT NULL,
    doc_type        TEXT NOT NULL CHECK (doc_type IN
        ('prior_rfp_response','spec_sheet','partner_enablement','sme_faq')),
    approval_status TEXT NOT NULL DEFAULT 'approved',
    chunk_text      TEXT NOT NULL,
    token_count     INT  NOT NULL,
    embedding       VECTOR(1024) NOT NULL,
    tsv             TSVECTOR GENERATED ALWAYS AS
                       (to_tsvector('english', chunk_text)) STORED,
    embedding_model TEXT NOT NULL,
    ingested_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS kb_chunks_vec_idx
    ON kb_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS kb_chunks_tsv_idx
    ON kb_chunks USING GIN  (tsv);
CREATE INDEX IF NOT EXISTS kb_chunks_doc_idx
    ON kb_chunks (source_doc);
"""


@contextmanager
def connect() -> Iterator[psycopg.Connection]:
    env = load_env()
    with psycopg.connect(env.pg_dsn, autocommit=False) as conn:
        register_vector(conn)
        yield conn


def bootstrap() -> None:
    """Create extension, table, and indexes if missing."""
    env = load_env()
    # Step 1: create the extension on a plain connection (vector type doesn't exist yet)
    with psycopg.connect(env.pg_dsn, autocommit=True) as plain_conn:
        with plain_conn.cursor() as cur:
            cur.execute(EXT_DDL)
    # Step 2: now vector type is registered; use normal connect() for table + indexes
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(TABLE_DDL)
        conn.commit()


def truncate_chunks() -> None:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE kb_chunks")
        conn.commit()


def chunk_count() -> int:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM kb_chunks")
            row = cur.fetchone()
            return int(row[0]) if row else 0
