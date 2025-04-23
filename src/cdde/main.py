"""
This module handles the main execution flow of the application.
"""
import yaml
import sys
from .addons_api import load_addons
from .git_clone import clone_repo
from .puml_observer import Observer, Modes
from .metric_result_observer import ResultObserver
from .metrics_calculator import MetricsCalculator, MetricsRepository
from .factory_expr_evaluator import FactoryExprEvaluator


class Main:
    """
    Main class that coordinates the execution of the program.
    """

    def __init__(self):
        self.language = ""
        self.expr_evaluators: list[tuple[str, dict]] = []
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

    def set_language(self, language: str) -> None:
        """
        Set the language of the PlantUML file.
        """
        self.language = language

    def set_expr_evaluator(self, yaml_filepath: str) -> None:
        """
        Set the language of the queries.
        """
        try:
            yaml_file = self._get_yaml_as_dict(yaml_filepath)
            expr_evaluator_name = yaml_file.pop("metrics-generator")
            self.expr_evaluators.append((expr_evaluator_name, yaml_file))
        except:
            print("Error: The yaml file is not valid.")
            sys.exit(1)
    
    def _generate_uml(self, directory: str) -> str:
        """
        Generate the PlantUML file.
        """
        return self.api.generators[self.language]().generate_plantuml(
            directory)

    def parse(self, file: str, mode: Modes) -> None:
        """
        Parse the PlantUML file.
        """
        observer = self._set_composable_obs(self.observers)
        filter = self.api.observers['filter'](observer)
        filter.set_mode(mode)
        parser = self.api.parsers['parsimonious'](filter)
        parser.parse_uml(file)

    def _set_composable_obs(self, observers: list) -> Observer:
        """
        Set the composable observers.
        """
        lst = []
        for observer in observers:
            lst.append(self.api.observers[observer]())
        return self.api.observers['composable'](lst)

    def delete_plantuml(self, file: str) -> None:
        """
        Delete the PlantUML file.
        """
        self.api.generators[self.language]().delete_plantuml(file)

    def run_queries(self) -> None:
        """
        Run the queries.
        """
        result_observer = self._set_result_obs(self.results_observers)
        factory_expr_evaluator = FactoryExprEvaluator()
        metrics_api = MetricsRepository()
        design_db = self.api.design_db['Neo4j']()
        for expr_eval_name, queries in self.expr_evaluators:
            expr_evaluator = factory_expr_evaluator.create_evaluator(
                expr_eval_name, self.api)
            metrics_calulator = MetricsCalculator(expr_evaluator, design_db,
                                                  result_observer, queries,
                                                  metrics_api)
            metrics_calulator.calc_all_expr()

    def _set_result_obs(self, res_obs: list) -> ResultObserver:
        """
        Set the result observers.
        """
        lst = []
        for result_observer in res_obs:
            lst.append(self.api.results_observers[result_observer]())
        return self.api.results_observers['res_composable'](lst)

    def clean_db(self) -> None:
        """
        Clean the database.
        """
        self.api.observers['Neo4j']().delete_all()

    def _get_yaml_as_dict(self, filepath: str) -> dict[str, str]:
        """
        Get the expression evaluator name from the file path.
        """
        with open(filepath, 'r', encoding="utf-8") as file:
            return yaml.load(file, Loader=yaml.SafeLoader)

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
        self.parse(archivo_plantuml_before, Modes.BEFORE)
        self.parse(archivo_plantuml_after, Modes.AFTER)

        # Run the queries
        self.run_queries()

        # Delete the plantuml file
        self.delete_plantuml(archivo_plantuml_before)
        self.delete_plantuml(archivo_plantuml_after)

        # Delete the temporary directories
        git_clone.delete_dir()
