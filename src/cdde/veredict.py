import json


class Veredict:

    def __init__(self):
        self.thresholds_path = "thresholds.json"
        self.results_path = "results.json"
        self.not_passed = []

    def evaluate(self) -> None:
        """
        Evaluate the results and create a veredict.
        """
        self._set_metrics_not_passed()
        for metric in self.not_passed:
            print(f"Metric '{metric}' did not pass the veredict.")

    def _set_metrics_not_passed(self) -> None:
        """
        Set the metrics that did not pass the veredict.
        """
        percentiles = self.get_thresholds()
        resultados = self.get_global_results()
        for metric, threshold in percentiles.items():
            resultado = resultados[metric]
            if resultado > threshold:
                self.not_passed.append(metric)

    def get_thresholds(self) -> dict[str, float]:
        """
        Get the thresholds from the thresholds.json file.
        """
        thresholds = {}
        try:
            with open(self.thresholds_path, 'r', encoding="utf-8") as file:
                thresholds = json.load(file)
        except FileNotFoundError:
            print(f"Thresholds file not found: {self.thresholds_path}")
        return thresholds

    def get_global_results(self) -> dict[str, float]:
        """
        Get the global results from the boxplot creator.
        """
        data = {}
        with open(self.results_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data['global']
