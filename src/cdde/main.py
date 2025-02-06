"""
This module handles the main execution flow of the application.
"""
from enum import StrEnum
from .api import load_addons
from .git_clone import clone_repo
from .puml_observer import Observer
from .result_observer import ResultObserver


class Modes(StrEnum):
    Before = "before"
    After = "after"


class Main:
    """
    Main class that coordinates the execution of the program.
    """

    def __init__(self):
        self.lenguage = ""
        self.queryl = ""
        self.observers = []
        self.results_observers = []
        self.api = None

    def set_api(self) -> None:
        """
        Set the API.
        """
        api = load_addons()
        self.api = api

    def set_observers(self, observer: str) -> None:
        """
        Set the dictionaries of objects.
        """
        self.observers.append(observer)

    def set_result_observers(self, result_observer: str) -> None:
        """
        Set the dictionaries of objects.
        """
        self.results_observers.append(result_observer)

    def set_lenguage(self, lenguage: str) -> None:
        """
        Set the language of the PlantUML file.
        """
        self.lenguage = lenguage

    def set_queryl(self, queryl: str) -> None:
        """
        Set the language of the queries.
        """
        self.queryl = queryl

    def _generate_uml(self, directory: str) -> str:
        """
        Generate the PlantUML file.
        """
        return self.api.generators[self.lenguage]().generate_plantuml(directory)

    def parse(self, file: str, mode: str) -> None:
        """
        Parse the PlantUML file.
        """
        observer = self._set_composable_obs(self.observers)
        filter = self.api.observers['filter'](observer)
        filter.set_mode(mode)
        parser = self.api.parsers['parsimonious'](filter)
        parser.parse_uml(file)

    def delete_plantuml(self, file: str) -> None:
        """
        Delete the PlantUML file.
        """
        self.api.generators[self.lenguage]().delete_plantuml(file)

    def run_queries(self) -> None:
        """
        Run the queries.
        """
        result_observer = self._set_result_obs(self.results_observers)
        self.api.result_queries[self.queryl](result_observer).resolve_query()

    def _set_composable_obs(self, observers: list) -> Observer:
        """
        Set the composable observers.
        """
        lst = []
        for observer in observers:
            lst.append(self.api.observers[observer]())
        return self.api.observers['composable'](lst)

    def _set_result_obs(self, res_obs: list) -> ResultObserver:
        """
        Set the result observers.
        """
        lst = []
        for result_observer in res_obs:
            lst.append(self.api.results_observers[result_observer]())
        return self.api.results_observers['composable'](lst)

    def clean_db(self) -> None:
        """
        Clean the database.
        """
        self.api.observers['Neo4j']().delete_all()

    def runCddE(self, repo_git: str, pr_number: int) -> None:
        """
        Run the main logic of the program.
        """
        # Git examples
        before, after, git_clone = clone_repo(repo_git, pr_number)
        # Generate the plantuml file
        archivo_plantuml_before = self._generate_uml(before)
        archivo_plantuml_after = self._generate_uml(after)

        # Clean the database
        self.clean_db()

        # Parse the plantuml file
        self.parse(archivo_plantuml_before, Modes.Before.value)
        self.parse(archivo_plantuml_after, Modes.After.value)

        # Run the queries
        self.run_queries()

        # Delete the plantuml file
        self.delete_plantuml(archivo_plantuml_before)
        self.delete_plantuml(archivo_plantuml_after)

        # Delete the temporary directories
        git_clone.delete_dir()
