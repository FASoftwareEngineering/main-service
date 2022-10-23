import typer

app = typer.Typer()


@app.command()
def example():
    """Пример простой CLI команды"""
    print("Just a simple CLI command")


if __name__ == "__main__":
    app()
