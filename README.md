# Poetry + Flask Project

### Install Poetry

Read the [Poetry Installation Guide](https://python-poetry.org/docs/#installation)

### Install Dependencies

```bash
poetry install
```

### Run with Flask (Dev)
```bash
poetry run flask --app audio_atlas_api run --debug
```

### Run with Gunicorn (Prod on Linux)
```bash
poetry run gunicorn --bind 0.0.0.0:5000 audio_atlas_api
```

### More info

- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Gunicorn](https://gunicorn.org/)
- [Poetry](https://python-poetry.org/)