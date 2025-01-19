import typer
from .main import Main
from enum import StrEnum
app = typer.Typer(name="CddE")

# "https://github.com/jfeliu007/goplantuml", 168  # GO (none changes)

# "https://github.com/jfeliu007/goplantuml", 145  # GO (many changes)


class Leng(StrEnum):
    """
    StrEnum for the lenguage.
    """
    py = ".py"
    go = ".go"
    cpp = ".cpp"


class Queryleng(StrEnum):
    """
    StrEnum for the query lenguage.
    """
    cypher = "cypher"


class Store(StrEnum):
    """
    StrEnum for the database.
    """
    Neo4j = "Neo4j"
    console = "console"

class FormatResult(StrEnum):
    """
    StrEnum for the format of the result.
    """
    json = "json"
    csv = "csv"
    console = "console"


def set_lenguage(lenguage: Leng, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if lenguage is not None:
        main.set_lenguage(lenguage.value)


def set_querylenguage(querylenguage: Queryleng, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if querylenguage is not None:
        main.set_queryl(querylenguage.value)


def add_observer(observer: Store, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if observer is not None:
        main.set_observers(observer.value)


def add_result_observer(result_observer: FormatResult, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if result_observer is not None:
        main.set_result_observers(result_observer.value)


@app.command()
def run(
    repo_git: str = typer.Argument(..., help="Repository to evaluate"),
    pr_number: int = typer.Argument(..., help="Pull request number"),
    leng: Leng = typer.Option(
        ".py", help="Selected lenguage of the repository"),
    queryl: Queryleng = typer.Option("cypher",
                                     help="Selected query lenguage of the repository"),
    store: Store = typer.Option("Neo4j", help="Selected graph database"),
    format_result: FormatResult = typer.Option(
        "json", help="Selected the format of the result")
):
    """Run the evaluation of the repository."""
    main = Main()
    main.set_api()
    set_lenguage(leng, main)
    set_querylenguage(queryl, main)
    add_observer(store, main)
    add_result_observer(format_result, main)

    main.runCddE(repo_git, pr_number)


if __name__ == "__main__":
    app()
