# Streamlit Web App

## Local Launch

```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

Open the URL Streamlit prints, usually `http://localhost:8501`.

## What It Shows

- The configured warehouse scenario from `configs/warehouse_delivery.json`.
- Q-learning controls and progress metrics.
- A Matplotlib map with shelves, zones, robot trail, target, and sensor rays.
- Reward history for completed episodes.

## Deploy

For Streamlit Cloud or similar platforms, use:

- Main file: `streamlit_app.py`
- Python dependencies: `requirements.txt`
- Optional process file: `Procfile`

`DEPLOY.md` has platform-specific notes.
