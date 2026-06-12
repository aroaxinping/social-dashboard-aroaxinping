"""
Load and normalize TikTok + Instagram analytics CSVs into a unified DataFrame.
Falls back to synthetic data when CSVs are not found.
"""

import pandas as pd
import numpy as np
from pathlib import Path

import os

# CSV paths — override with env vars or pass directly
# TIKTOK_CSV_PATH and INSTAGRAM_CSV_PATH env vars take priority
TIKTOK_CSV = Path(os.environ.get("TIKTOK_CSV_PATH", "data/videos_engagement.csv"))
INSTAGRAM_CSV = Path(os.environ.get("INSTAGRAM_CSV_PATH", "data/reels_metricas.csv"))


def load_tiktok(path: Path = TIKTOK_CSV) -> pd.DataFrame:
    """Load TikTok CSV and normalize columns."""
    df = pd.read_csv(path)
    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    return df.assign(
        date=df["published_date"],
        platform="TikTok",
        title=df["title"].str.strip(),
        views=pd.to_numeric(df["views"], errors="coerce").fillna(0).astype(int),
        likes=pd.to_numeric(df["likes"], errors="coerce").fillna(0).astype(int),
        comments=pd.to_numeric(df["comments"], errors="coerce").fillna(0).astype(int),
        shares=pd.to_numeric(df["shares"], errors="coerce").fillna(0).astype(int),
        saves=pd.to_numeric(df["saves"], errors="coerce").fillna(0).astype(int),
        followers_gained=pd.to_numeric(df["new_followers"], errors="coerce").fillna(0).astype(int),
        engagement_rate=pd.to_numeric(df["engagement_rate_pct"], errors="coerce").fillna(0),
        topic=df["topic"].fillna("Sin tema"),
    )


def load_instagram(path: Path = INSTAGRAM_CSV) -> pd.DataFrame:
    """Load Instagram CSV and normalize columns."""
    df = pd.read_csv(path)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    return df.assign(
        date=df["fecha"],
        platform="Instagram",
        title=df["descripcion_corta"].str.strip().str[:80],
        views=pd.to_numeric(df["visualizaciones"], errors="coerce").fillna(0).astype(int),
        likes=pd.to_numeric(df["me_gustas"], errors="coerce").fillna(0).astype(int),
        comments=pd.to_numeric(df["comentarios"], errors="coerce").fillna(0).astype(int),
        shares=pd.to_numeric(df["compartidos"], errors="coerce").fillna(0).astype(int),
        saves=pd.to_numeric(df["guardados"], errors="coerce").fillna(0).astype(int),
        followers_gained=pd.to_numeric(df["seguidores_ganados"], errors="coerce").fillna(0).astype(int),
        engagement_rate=pd.to_numeric(df["engagement_rate"], errors="coerce").fillna(0),
        topic=df["tema"].fillna("Sin tema"),
    )


UNIFIED_COLS = [
    "date", "platform", "title", "views", "likes", "comments",
    "shares", "saves", "followers_gained", "engagement_rate", "topic",
]


def generate_synthetic() -> pd.DataFrame:
    """Generate synthetic data for demo / Streamlit Cloud deploy."""
    rng = np.random.default_rng(42)
    n = 60
    dates = pd.date_range("2026-01-01", periods=n, freq="2D")
    topics = ["Tech humor", "Data Science", "Setup / desk", "Tutorial", "Humor personal / relatable"]
    platforms = rng.choice(["TikTok", "Instagram"], size=n)

    views = rng.integers(500, 900_000, size=n)
    likes = (views * rng.uniform(0.03, 0.25, size=n)).astype(int)
    comments = (views * rng.uniform(0.001, 0.01, size=n)).astype(int)
    shares = (views * rng.uniform(0.005, 0.04, size=n)).astype(int)
    saves = (views * rng.uniform(0.002, 0.02, size=n)).astype(int)
    total = likes + comments + shares + saves

    return pd.DataFrame({
        "date": dates,
        "platform": platforms,
        "title": [f"video_{i}" for i in range(n)],
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "saves": saves,
        "followers_gained": rng.integers(0, 50, size=n),
        "engagement_rate": np.round(total / views * 100, 2),
        "topic": rng.choice(topics, size=n),
    })


def load_all() -> pd.DataFrame:
    """Load real CSVs if available, otherwise synthetic fallback."""
    frames = []

    try:
        frames.append(load_tiktok()[UNIFIED_COLS])
    except FileNotFoundError:
        pass

    try:
        frames.append(load_instagram()[UNIFIED_COLS])
    except FileNotFoundError:
        pass

    if not frames:
        return generate_synthetic()

    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["date"]).sort_values("date", ascending=False).reset_index(drop=True)
    return df
