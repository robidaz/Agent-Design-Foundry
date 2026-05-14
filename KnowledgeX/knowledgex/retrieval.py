"""Hybrid retrieval: pgvector cosine + tsvector BM25-style, fused via RRF.

Single Postgres round-trip per question. Each channel (vector, BM25) is ranked
independently and the two rank lists are fused via Reciprocal Rank Fusion with
constant rrf_k (Cormack/Clarke). Final list is filtered to top_k rows whose
top vector similarity meets min_vector_similarity; empty result → caller treats
the question as NO_SOURCE.
"""

from __future__ import annotations

from knowledgex import db
from knowledgex.config import load_config
from knowledgex.embeddings import embed_one
from knowledgex.schemas import RetrievedChunk

_SEARCH_SQL = """
WITH vec AS (
  SELECT chunk_id, 1 - (embedding <=> %(qvec)s::vector) AS sim_score,
         ROW_NUMBER() OVER (ORDER BY embedding <=> %(qvec)s::vector) AS rnk
  FROM kb_chunks
  ORDER BY embedding <=> %(qvec)s::vector
  LIMIT %(overfetch)s
),
bm AS (
  SELECT chunk_id,
         ts_rank_cd(tsv, plainto_tsquery('english', %(qtxt)s)) AS bm_score,
         ROW_NUMBER() OVER (
           ORDER BY ts_rank_cd(tsv, plainto_tsquery('english', %(qtxt)s)) DESC
         ) AS rnk
  FROM kb_chunks
  WHERE tsv @@ plainto_tsquery('english', %(qtxt)s)
  ORDER BY bm_score DESC
  LIMIT %(overfetch)s
),
fused AS (
  SELECT
    c.chunk_id,
    c.source_doc,
    c.doc_type,
    c.chunk_text,
    COALESCE(v.sim_score, 0.0)                            AS sim_score,
    COALESCE(b.bm_score, 0.0)                             AS bm_score,
    COALESCE(1.0 / (%(rrf_k)s + v.rnk), 0.0)
      + COALESCE(1.0 / (%(rrf_k)s + b.rnk), 0.0)          AS rrf_score
  FROM kb_chunks c
  LEFT JOIN vec v USING (chunk_id)
  LEFT JOIN bm  b USING (chunk_id)
  WHERE v.chunk_id IS NOT NULL OR b.chunk_id IS NOT NULL
)
SELECT chunk_id, source_doc, doc_type, chunk_text, sim_score, bm_score, rrf_score
FROM fused
ORDER BY rrf_score DESC
LIMIT %(topk)s;
"""


def search(question_text: str) -> list[RetrievedChunk]:
    cfg = load_config()
    qvec = embed_one(question_text, input_type="query")

    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _SEARCH_SQL,
                {
                    "qvec": qvec,
                    "qtxt": question_text,
                    "overfetch": cfg.retrieval.overfetch,
                    "rrf_k": cfg.retrieval.rrf_k,
                    "topk": cfg.retrieval.top_k,
                },
            )
            rows = cur.fetchall()

    results = [
        RetrievedChunk(
            chunk_id=row[0],
            source_doc=row[1],
            doc_type=row[2],
            chunk_text=row[3],
            similarity_score=float(row[4]),
            bm25_score=float(row[5]),
            rrf_score=float(row[6]),
        )
        for row in rows
    ]

    # Apply min_vector_similarity gate: if the top chunk is below the floor,
    # treat the whole result set as NO_SOURCE.
    if not results or results[0].similarity_score < cfg.retrieval.min_vector_similarity:
        return []
    return results
