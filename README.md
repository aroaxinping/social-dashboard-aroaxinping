# social-dashboard-aroaxinping

Dashboard de analytics para TikTok e Instagram. Visualiza KPIs, engagement por tema y comparativa entre plataformas.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Datos

Lee CSVs procesados de:
- `~/Desktop/tiktok-analytics-aroaxinping/data/processed/videos_engagement.csv`
- `~/Desktop/instagram-analytics-aroaxinping/data/processed/reels_metricas.csv`

Si no encuentra los CSVs genera datos sinteticos para demo.

## Deploy en Streamlit Cloud

1. Fork o push a GitHub
2. Conectar repo en [share.streamlit.io](https://share.streamlit.io)
3. Main file: `app.py`

Sin CSVs locales usara datos sinteticos automaticamente.

## Stack

Streamlit, Pandas, Plotly, NumPy.
