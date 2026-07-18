# Deployment

## Local Streamlit

```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

## Streamlit Cloud

1. Push this project to GitHub.
2. Create a new app at `https://share.streamlit.io`.
3. Select the repository.
4. Set the main file to `streamlit_app.py`.
5. Deploy.

## Heroku/Railway-Style Platforms

The repo includes:

- `Procfile`
- `setup.sh`
- `requirements.txt`
- `packages.txt`

The process command is:

```bash
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

## Notes

The web app uses Matplotlib for rendering, so the code sets `MPLCONFIGDIR` to a local writable cache directory. This avoids permission issues on locked-down hosts.
