"""Config loader: assets/config.yaml + env vars → frozen Pydantic settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class RetrievalConfig(BaseModel):
    top_k: int = 5
    overfetch: int = 20             # per-channel pool size before RRF
    rrf_k: int = 60                 # Cormack/Clarke RRF constant
    min_vector_similarity: float = 0.55


class ScoringConfig(BaseModel):
    high_sim: float = 0.65
    medium_sim: float = 0.60
    agreement_low: float = 0.55     # cheap-cosine: below → forward to Claude
    agreement_high: float = 0.85    # cheap-cosine: above → auto-agree


class ChunkingConfig(BaseModel):
    target_tokens: int = 400
    overlap_tokens: int = 50


class ModelsConfig(BaseModel):
    embedding_model: str = "BAAI/bge-large-en-v1.5"   # local; sentence-transformers
    embedding_dim: int = 1024
    claude_model: str = "claude-sonnet-4-6"


class AppConfig(BaseModel):
    retrieval: RetrievalConfig = RetrievalConfig()
    scoring: ScoringConfig = ScoringConfig()
    chunking: ChunkingConfig = ChunkingConfig()
    models: ModelsConfig = ModelsConfig()


class EnvSettings(BaseSettings):
    """Env-sourced secrets + connection strings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anthropic_api_key: str = ""
    pg_dsn: str = "postgresql://knowledgex:knowledgex@localhost:5432/knowledgex"


@lru_cache(maxsize=1)
def load_config(path: Path | None = None) -> AppConfig:
    cfg_path = path or (ROOT / "assets" / "config.yaml")
    if not cfg_path.exists():
        return AppConfig()
    raw = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    return AppConfig.model_validate(raw)


@lru_cache(maxsize=1)
def load_env() -> EnvSettings:
    return EnvSettings()
