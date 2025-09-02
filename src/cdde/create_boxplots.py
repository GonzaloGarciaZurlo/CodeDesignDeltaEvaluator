import matplotlib.pyplot as plt
import os
import json
from typing import Generator
import numpy as np


class BoxPlotCreator:

    def __init__(self, json_path: str):
        self.json_path = json_path

    def _open_json(self, file_path: str) -> dict:
        """
        Open the json file.
        """
        data = {}
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
        return data

    def get_results_of_each_metric(self) -> Generator[str, list[float], None]:
        """
        Get the results of each metric from the json file.
        """
        data = self._open_json(self.json_path)
        global_results = data.get("global", {})
        for metric, values in global_results.items():
            yield metric, values

    def create_boxplots(self):
        """
        Create all boxplots in the same figure
        """
        results = list(self.get_results_of_each_metric())
        labels = [metric for metric, _ in results]
        data = [values for _, values in results]

        plt.figure(figsize=(14, 6))
        plt.boxplot(data, tick_labels=labels, vert=True, patch_artist=True)

        plt.title("Boxplot of Code Design Metrics")
        plt.xlabel("Metrics")
        plt.ylabel("Values")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig("boxplot.png", dpi=300, bbox_inches="tight")
        plt.close()

    def get_percentiles_90(self) -> dict[str, float]:
        """
        Calcula el percentil 90 para cada métrica global.
        - Ignora None/NaN.
        - Si no hay datos para una métrica, devuelve 0.0 (ajustá si preferís None).
        """
        percentiles: dict[str, float] = {}
        for metric, values in self.get_results_of_each_metric():
            if values:
                p = self.conditional_percentile(values, 90)
            else:
                p = 0.0
            percentiles[metric] = p
        return percentiles

    def conditional_percentile(self, data: list[float], percentile: float) -> float:
        """
        Calculate the conditional percentile:
        If the 90% or more of the values are 0, then calculate the percentile n of the remaining values.
        """
        if sum(1 for x in data if x == 0) / len(data) >= 0.9:
            # If 90% or more are 0, calculate the percentile of the remaining values
            remaining = [x for x in data if x != 0]
            if not remaining:
                return 0.0
            return float(np.percentile(remaining, percentile))
        return float(np.percentile(data, percentile))

    def store_percentiles_90(self, output_path: str = "thresholds.json") -> None:
        """
        Store the 90th percentiles in a json file.
        """
        percentiles = self.get_percentiles_90()
        self._delete_existing_file(output_path)
        with open(output_path, 'w', encoding="utf-8") as file:
            json.dump(percentiles, file, indent=4)

    def _delete_existing_file(self, file_path: str) -> None:
        """
        Delete the existing file if it exists.
        """
        if os.path.exists(file_path):
            os.remove(file_path)


boxplot_creator = BoxPlotCreator("multiples_results.json")
boxplot_creator.store_percentiles_90()
