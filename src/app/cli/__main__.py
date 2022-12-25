import typer

from app.cli import db
from app.config import config
from app.core.db import db as _db

_db.configure(config)

app = typer.Typer()
app.add_typer(db.app, name="db")

if __name__ == "__main__":
    app()
