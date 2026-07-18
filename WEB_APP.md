# Web UI

## Standalone UI

Open:

```bash
open web/index.html
```

This dependency-free browser UI includes:

- Canvas scenario map with shelves, zones, robot trail, target, and sensor rays.
- Q-learning controls, episode stepping, reward metrics, and reward chart.
- Build mode for selecting or placing shelves, zones, robot start, and target.
- JSON editing, copy, and download for scenario files.

## Streamlit UI

Run the Python-backed browser demo with:

```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

The Streamlit app loads `configs/warehouse_delivery.json` and shows:

- Scenario map with shelves, zones, target, robot trail, and sensor rays.
- Metrics for episode, step, reward, arrivals, exploration, and known states.
- Reward history across completed episodes.
- Controls for Q-learning, sensor rays, stepping, continuous run, reset, and run episode.

For deployment notes, see `DEPLOY.md` or `README_WEBAPP.md`.
