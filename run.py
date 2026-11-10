"""Entry point: `flask run` (FLASK_APP=run.py) or gunicorn run:app."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
