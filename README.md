# social-dashboard-aroaxinping

Streamlit dashboard that aggregates TikTok and Instagram analytics into a single view.
Reads processed CSVs from your local exports — falls back to synthetic demo data if no files are found.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data

The dashboard reads two CSVs with processed analytics exports:

| Platform | Expected columns |
|---|---|
| TikTok | `published_date`, `title`, `views`, `likes`, `comments`, `shares`, `saves`, `new_followers`, `engagement_rate_pct`, `topic` |
| Instagram | `fecha`, `descripcion_corta`, `visualizaciones`, `me_gustas`, `comentarios`, `compartidos`, `guardados`, `seguidores_ganados`, `engagement_rate`, `tema` |

**Override paths with environment variables:**

```bash
export TIKTOK_CSV_PATH=path/to/tiktok.csv
export INSTAGRAM_CSV_PATH=path/to/instagram.csv
streamlit run app.py
```

If no CSVs are found, the app generates synthetic data automatically so you can see the dashboard without real data.

## Deploy on Streamlit Cloud

1. Push to GitHub
2. Connect repo at [share.streamlit.io](https://share.streamlit.io)
3. Main file: `app.py`

Without CSVs, Streamlit Cloud will use synthetic data.

## Stack

Python · Streamlit · Plotly · pandas · NumPy
