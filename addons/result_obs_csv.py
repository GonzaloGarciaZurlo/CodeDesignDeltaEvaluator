"""
This module contains the ResultCSV class,
which is an Observer that saves the information it receives in a CSV file.
"""
import subprocess
from overrides import override
from api import CddeAPI
from result_observer import ResultObserver


class ResultCSV(ResultObserver):
    """
    Observer that saves the information it receives in a CSV file.
    """
    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened,
        creating the CSV file.
        """
        self._create_csv()

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed,
        deleting the CSV file.
        """
        # self._delete_csv()

    @override
    def on_result_metric_found(self, result: int, kind: str, class_name: str) -> None:
        """
        Save the result found in the CSV file.
        with the format: kind, result, without spaces.
        """
        self._write_csv(result, kind, class_name)

    @override
    def on_result_data_found(self, result: str, kind: str) -> None:
        """
        Save the result found in the CSV file.
        with the format: kind, result, without spaces.
        """
        self._write_csv(result, kind, "Data")

    def _create_csv(self) -> None:
        """
        Create the CSV file. If it already exists, delete it first.
        """
        subprocess.run("rm -f results.csv && touch results.csv",
                       shell=True, check=True)

    def _write_csv(self, result: int | str, kind: str, class_name: str) -> None:
        """
        Write the result in the CSV file.
        """
        subprocess.run(f"echo '{class_name},{kind},{
                       result}' >> results.csv", shell=True, check=True)

    def _delete_csv(self) -> None:
        """
        Delete the CSV file.
        """
        subprocess.run("rm results.csv", shell=True, check=True)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_observer('csv', ResultCSV)
