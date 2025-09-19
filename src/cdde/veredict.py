"""
This module evaluates the results and creates a veredict."""
import json


class Veredict:
    """
    Class to evaluate the results and create a veredict."""

    def __init__(self):
        self.thresholds_path = "thresholds.json"
        self.results_path = "results.json"
        self.not_passed: list[tuple[str, float, float]] = []

    def evaluate(self) -> None:
        """
        Evaluate the results and create a veredict.
        """
        self._set_metrics_not_passed()
        for metric, magnitude, ratio in self.not_passed:
            print(
                f"""Metric '{metric}' with magnitude '{magnitude}' and ratio
                '{ratio}' did not pass the veredict.""")

        veredict = self.norm_p(self.not_passed, 2)
        print(f"Veredict (L2 norm): {veredict}")

    def _set_metrics_not_passed(self) -> None:
        """
        Set the metrics that did not pass the veredict.
        """
        percentiles = self.get_thresholds()
        results = self.get_global_results()
        for metric, result in results.items():
            magnitude = metric[-1:]
            metric = metric[:-2]
            threshold = percentiles[metric]
            if result > threshold:
                if threshold == 0:
                    ratio = 10  # ver
                    self.not_passed.append((metric, int(magnitude), ratio))
                else:
                    self.not_passed.append(
                        (metric, int(magnitude), result/threshold))

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

    @staticmethod
    def norm_p(args: list[tuple[str, float, float]], p: int) -> float:
        """
        Calculate weighted L^p norm for the metrics.
        Each arg is (metric, weight, ratio).
        """
        if not args:
            return 0.0

        total = sum(weight * (ratio ** p) for _, weight, ratio in args)
        return total ** (1 / p)
