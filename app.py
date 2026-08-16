"""
Social Dashboard - @aroaxinping
TikTok + Instagram analytics in one place.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.load_data import load_all

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="@aroaxinping analytics",
    page_icon="📊",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────

ACCENT_ORANGE = "#e85d04"
ACCENT_BLUE = "#6a9ad4"
BG = "#0f0f0f"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'JetBrains Mono', monospace;
    }}
    .stMetric label {{
        color: {ACCENT_BLUE} !important;
        font-size: 0.85rem !important;
    }}
    .stMetric [data-testid="stMetricValue"] {{
        color: {ACCENT_ORANGE} !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stSidebar"] {{
        background-color: #111111;
    }}
    h1, h2, h3 {{
        color: {ACCENT_ORANGE} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def get_data() -> pd.DataFrame:
    return load_all()

df = get_data()

# ── Sidebar filters ──────────────────────────────────────────────────────────

st.sidebar.title("filtros")

# Date range
min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input(
    "rango de fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Platform
platforms = st.sidebar.multiselect(
    "plataforma",
    options=sorted(df["platform"].unique()),
    default=sorted(df["platform"].unique()),
)

# Topic
topics = st.sidebar.multiselect(
    "tema",
    options=sorted(df["topic"].unique()),
    default=sorted(df["topic"].unique()),
)

# ── Apply filters ────────────────────────────────────────────────────────────

mask = (
    df["platform"].isin(platforms)
    & df["topic"].isin(topics)
)

if len(date_range) == 2:
    start, end = date_range
    mask = mask & (df["date"].dt.date >= start) & (df["date"].dt.date <= end)

filtered = df[mask].copy()

# ── Header ───────────────────────────────────────────────────────────────────

st.title("@aroaxinping")
st.caption("tiktok + instagram analytics dashboard")

# ── KPIs ─────────────────────────────────────────────────────────────────────

total_views = int(filtered["views"].sum())
avg_engagement = round(filtered["engagement_rate"].mean(), 2) if len(filtered) else 0
total_followers = int(filtered["followers_gained"].sum())
total_posts = len(filtered)

k1, k2, k3, k4 = st.columns(4)
k1.metric("total views", f"{total_views:,}")
k2.metric("avg engagement %", f"{avg_engagement}")
k3.metric("followers gained", f"{total_followers:,}")
k4.metric("posts", f"{total_posts}")

st.divider()

# ── Chart: Views over time ───────────────────────────────────────────────────

st.subheader("views over time")

if not filtered.empty:
    daily = (
        filtered.groupby([pd.Grouper(key="date", freq="W"), "platform"])["views"]
        .sum()
        .reset_index()
    )
    fig_views = px.area(
        daily,
        x="date",
        y="views",
        color="platform",
        color_discrete_map={"TikTok": ACCENT_ORANGE, "Instagram": ACCENT_BLUE},
        template="plotly_dark",
    )
    fig_views.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font_family="JetBrains Mono, monospace",
        legend=dict(orientation="h", y=-0.15),
        margin=dict(l=20, r=20, t=10, b=40),
    )
    st.plotly_chart(fig_views, use_container_width=True)
else:
    st.info("No hay datos para el rango seleccionado.")

# ── Charts row: engagement by topic + platform comparison ────────────────────

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("engagement by topic")
    if not filtered.empty:
        topic_eng = (
            filtered.groupby("topic")["engagement_rate"]
            .mean()
            .sort_values(ascending=True)
            .reset_index()
        )
        fig_topic = px.bar(
            topic_eng,
            x="engagement_rate",
            y="topic",
            orientation="h",
            color_discrete_sequence=[ACCENT_ORANGE],
            template="plotly_dark",
        )
        fig_topic.update_layout(
            paper_bgcolor=BG,
            plot_bgcolor=BG,
            font_family="JetBrains Mono, monospace",
            xaxis_title="avg engagement %",
            yaxis_title="",
            margin=dict(l=20, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_topic, use_container_width=True)

with col_right:
    st.subheader("platform comparison")
    if not filtered.empty:
        plat = (
            filtered.groupby("platform")
            .agg(views=("views", "sum"), engagement=("engagement_rate", "mean"), posts=("title", "count"))
            .reset_index()
        )
        fig_plat = go.Figure()
        fig_plat.add_trace(go.Bar(
            name="views (k)",
            x=plat["platform"],
            y=plat["views"] / 1000,
            marker_color=ACCENT_ORANGE,
        ))
        fig_plat.add_trace(go.Bar(
            name="avg engagement %",
            x=plat["platform"],
            y=plat["engagement"],
            marker_color=ACCENT_BLUE,
        ))
        fig_plat.update_layout(
            barmode="group",
            template="plotly_dark",
            paper_bgcolor=BG,
            plot_bgcolor=BG,
            font_family="JetBrains Mono, monospace",
            legend=dict(orientation="h", y=-0.15),
            margin=dict(l=20, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_plat, use_container_width=True)

# ── Top posts table ──────────────────────────────────────────────────────────

st.divider()
st.subheader("top posts")

if not filtered.empty:
    top = (
        filtered.nlargest(15, "views")[
            ["date", "platform", "title", "views", "likes", "engagement_rate", "topic"]
        ]
        .reset_index(drop=True)
    )
    top["date"] = top["date"].dt.strftime("%Y-%m-%d")
    st.dataframe(top, use_container_width=True, hide_index=True)

# ── Footer ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption("hecho con streamlit + plotly | @aroaxinping")
