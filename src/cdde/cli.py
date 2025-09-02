"""
This module is the CLI of the tool.
It uses the Typer library to create the CLI. 
"""
from typing import List
from enum import StrEnum
import typer
from .main import Main

app = typer.Typer(name="cdde")
"GO REPOSITORIES"

# cdde https://github.com/stretchr/testify/pulls 1775 src/queries/cypher.yml src/queries/derived_metrics.yml --lang go --v
# cdde https://github.com/sirupsen/logrus 1449 src/queries/cypher.yml src/queries/derived_metrics.yml --lang go --v
# cdde https://github.com/spf13/cobra --main-branch main 2294 src/queries/cypher.yml src/queries/derived_metrics.yml --lang go --v
# cdde https://github.com/jfeliu007/goplantuml 168 src/queries/cypher.yml src/queries/derived_metrics.yml --lang go --v
# cdde https://github.com/jfeliu007/goplantuml 145 src/queries/cypher.yml src/queries/derived_metrics.yml --lang go --v

class Lang(StrEnum):
    """
    StrEnum for the language.
    """
    PY = "py"
    GO = "go"
    CPP = "cpp"


class Store(StrEnum):
    """
    StrEnum for the database.
    """
    NEO4J = "Neo4j"


class FormatResult(StrEnum):
    """
    StrEnum for the format of the result.
    """
    JSON = "json"
    CSV = "csv"
    CONSOLE = "console"


def set_language(language: Lang, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if language is not None:
        main.set_language(language.value)


def add_yamls(yamls: list[str], main: Main) -> None:
    """
    Set the options of the tool.
    """
    for yaml_filepath in yamls:
        main.set_expr_evaluator(yaml_filepath)


def add_observer(observer: List[Store], main: Main) -> None:
    """
    Set the options of the tool.
    """
    for obs in observer:
        if obs is not None:
            main.set_observers(obs.value)


def add_visual_mode(visual: bool, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if visual:
        main.set_observers('printer')


def add_result_observer(result_observer: List[FormatResult],
                        main: Main) -> None:
    """
    Set the options of the tool.
    """
    for res_obs in result_observer:
        if res_obs is not None:
            if res_obs.value == "console":
                main.set_result_observers("res_printer")
            else:
                main.set_result_observers(res_obs.value)


def set_json_to_multiple_metrics(main: Main) -> None:
    """
    Set the JSON output to multiple metrics.
    """
    main.set_result_observers(FormatResult.JSON.value)
    main.set_thresholds = True


@app.command()
def CddE(
        repo_git: str = typer.Argument(
            ..., help="Link to the repository to evaluate"),
        main_branch: str = typer.Option("master",
                                        help="Main branch of the repository"),
        pr_number: int = typer.Argument(..., help="Pull request number"),
        yamls: List[str] = typer.Argument(
            ..., help="Select the file with the queries"),
        lang: Lang = typer.Option(Lang.PY.value,
                                  help="Select language of the repository"),
        store: List[Store] = typer.Option([Store.NEO4J],
                                          help="Select graph database"),
        set_thresholds: bool = typer.Option(
            False,
            "--set-thresholds",
            help="Set thresholds for the evaluation"),
        visual: bool = typer.
    Option(
        False,
        "--visual",
        "--v",
        help=
        "Visualize the class and relations of the repository on the console"),
        format_result: List[FormatResult] = typer.Option(
            [FormatResult.JSON.value],
            help="Select the format of the result")):
    """Run the tool CddE"""
    main = Main()
    main.set_api()
    set_language(lang, main)
    add_yamls(yamls, main)
    add_observer(store, main)
    add_visual_mode(visual, main)
    add_result_observer(format_result, main)

    if set_thresholds:
        set_json_to_multiple_metrics(main)
        main.runSetThresholds(repo_git, main_branch)

    else:
        main.runCddE(repo_git, main_branch, pr_number)
