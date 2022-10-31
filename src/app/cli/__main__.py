import typer

from app.cli import db

app = typer.Typer()
app.add_typer(db.app, name="db")

if __name__ == "__main__":
    app()
