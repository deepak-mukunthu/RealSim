# Start Here

## Fastest Path

```bash
source venv/bin/activate
python app.py
```

The desktop app opens the starter warehouse scenario from `configs/warehouse_delivery.json`. Use `Start`, `Pause`, `Reset`, `New Episode`, `Steps/frame`, `Sensor Rays`, and the `Training` toggle.

## Visual RL Training

```bash
source venv/bin/activate
python examples/visual_scenario_trainer.py
```

For a fast terminal-only run:

```bash
python examples/visual_scenario_trainer.py --no-render --episodes 30
```

## Browser Demo

```bash
open web/index.html
streamlit run streamlit_app.py
```

## Customize The World

Copy the starter scenario and edit the JSON:

```bash
cp configs/warehouse_delivery.json configs/my_scenario.json
python examples/visual_scenario_trainer.py --scenario configs/my_scenario.json
```

Read `README.md`, `QUICKSTART.md`, and `docs/ARCHITECTURE.md` for the full project shape.
