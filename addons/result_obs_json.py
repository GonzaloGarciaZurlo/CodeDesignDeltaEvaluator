"""
This module contains the ResultJson class,
which is an Observer that saves the information it receives in a Json file.
"""
import subprocess
import json
import os
from overrides import override
from api import CddeAPI
from result_observer import ResultObserver


class ResultJson(ResultObserver):
    """
    Observer that saves the information it receives in a Json file.
    """
    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened,
        creating the Json file.
        """
        self._create_json()

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed,
        deleting the Json file.
        """
        # self._delete_json()

    @override
    def on_result_metric_found(self, result: int, kind: str, class_name) -> None:
        """
        Save the result found in the Json file.
        with the format: kind, result, without spaces.
        """
        self._write_json(result, kind, class_name)

    @override
    def on_result_data_found(self, result: str, kind: str) -> None:
        """
        In this case, the result is not saved in the Json file.
        """
        self._write_json("Data", kind, result)

    def _create_json(self) -> None:
        """
        Create the Json file. If it already exists, delete it first.
        """
        subprocess.run("rm -rf results.json && touch results.json",
                       shell=True, check=True)

    def _write_json(self, result: int | str, kind: str, class_name: str) -> None:
        """
        Write the result in the Json file.
        """
        file_path = 'results.json'

        data = self._open_json(file_path)

        if kind not in data:
            data[kind] = {}
        data[kind][class_name] = result

        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def _open_json(self, file_path: str) -> dict:
        """
        Open the json file.
        """
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
        else:
            data = {}
        return data

    def _delete_json(self) -> None:
        """
        Delete the json file.
        """
        subprocess.run("rm results.json", shell=True, check=True)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_observer('json', ResultJson)
