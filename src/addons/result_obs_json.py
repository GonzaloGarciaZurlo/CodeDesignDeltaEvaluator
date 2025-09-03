"""
This module contains the ResultJson class,
which is an Observer that saves the information it receives in a Json file.
"""
import subprocess
import json
import os
from overrides import override
from src.cdde.addons_api import CddeAPI
from src.cdde.metric_result_observer import ResultObserver
from src.cdde.metrics_calculator import TypeMetrics


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

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed,
        deleting the Json file.
        """
        if self.set_thresholds:
            self._delete_per_clases_and_per_package()

    def _delete_per_clases_and_per_package(self) -> None:
        """
        Delete the per_classes and per_package keys from the Json file.
        """
        file_path = 'results.json'

        data = self._open_json(file_path)

        if TypeMetrics.PER_CLASS in data:
            del data[TypeMetrics.PER_CLASS]
        if TypeMetrics.PER_PACKAGE in data:
            del data[TypeMetrics.PER_PACKAGE]

        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @override
    def on_result_metric_found(self, result: int, kind: str,
                               class_name: str, magnitude: int = 0) -> None:
        """
        Save the result found in the Json file.
        with the format: kind, result, without spaces.
        """
        if self.set_thresholds:
            self._write_multiples_json(result, kind, class_name)
        else:
            self._write_json(result, kind, class_name, magnitude=magnitude)

    @override
    def on_result_data_found(self, result: str, kind: str) -> None:
        """
        In this case, the result is not saved in the Json file.
        """
        if self.set_thresholds:
            self._write_multiples_json("Data", kind, result)
        else:
            self._write_json("Data", kind, result)

    def _create_json(self) -> None:
        """
        Create the Json file. If it already exists, delete it first.
        """
        subprocess.run("rm -rf results.json && touch results.json",
                       shell=True,
                       check=True)

    def _write_json(self, result: int | str, kind: str,
                    class_name: str, file_path: str = 'results.json', magnitude: int = 0) -> None:
        """
        Write the result in the Json file.
        """
        data = self._open_json(file_path)

        if kind not in data:
            data[kind] = {}
        data[kind][class_name + '_' + str(magnitude)] = result

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
            self._create_json()
            data = {}
        return data

    @override
    def delete_file(self) -> None:
        """
        Delete the json file.
        """
        subprocess.run("rm -rf results.json", shell=True, check=True)

    def _write_multiples_json(self, result: int | str, kind: str,
                              class_name: str, file_path: str = 'multiples_results.json') -> None:
        """
        Write the result in the Json file ot this form:
        {
            "global": {
                "class_name": [result1, result2, ...]
            }
        }
        where result1 is the first execution of the tool, result2 is the second execution, and so on (only in global key).
        """
        data = self._open_json(file_path)
        if kind != TypeMetrics.GLOBAL:
            self._write_json(result, kind, class_name, file_path)
        else:
            if kind not in data:
                data[kind] = {}
            if class_name not in data[kind]:
                data[kind][class_name] = []
            data[kind][class_name].append(result)
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_observer('json', ResultJson)
