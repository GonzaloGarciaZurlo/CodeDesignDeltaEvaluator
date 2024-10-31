"""
This module contains the ResultCSV class,
which is an Observer that saves the information it receives in a CSV file.
"""
from overrides import override
from api import CddeAPI
from result_observer import ResultObserver
import subprocess


class ResultCSV(ResultObserver):
    """
    Observer that saves the information it receives in a CSV file
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
        self._delete_csv()

    @override
    def on_result_found(self, result: str, kind: str) -> None:
        """
        Save the result found in the CSV file.
        with the format: kind, result, without spaces.
        """
        self._write_csv(result, kind)

    def _create_csv(self) -> None:
        """
        Create the CSV file.
        """
        subprocess.run("touch results.csv", shell=True)

    def _write_csv(self, result: str, kind: str) -> None:
        """
        Write the result in the CSV file.
        """
        subprocess.run(f"echo '{kind},{result}' >> results.csv", shell=True)

    def _delete_csv(self) -> None:
        """
        Delete the CSV file.
        """
        subprocess.run("rm results.csv", shell=True)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_observer('csv', ResultCSV)
