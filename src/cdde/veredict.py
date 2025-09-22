"""
This module evaluates the results and creates a veredict."""
import json

MODE_RESTRICTED = 25
MODE_DEFAULT = 35
MODE_UNRESTRICTED = 45


class Veredict:
    """
    Class to evaluate the results and create a veredict."""

    def __init__(self):
        self.global_threshold = 50.0
        self.thresholds_path = "thresholds.json"
        self.results_path = "results.json"
        self.thresholds = self.get_thresholds()
        self.results = self.get_global_results()
        self.not_passed: list[tuple[str, float, float]] = []

    def set_global_threshold(self, mode: str) -> None:
        """
        Set the global threshold.
        """
        if mode == "restricted":
            self.global_threshold = MODE_RESTRICTED
        elif mode == "default":
            self.global_threshold = MODE_DEFAULT
        elif mode == "unrestricted":
            self.global_threshold = MODE_UNRESTRICTED

    def evaluate(self) -> None:
        """
        Evaluate the results and create a veredict.
        """
        self._set_metrics_not_passed()

        print("\nMetrics that exceeded their threshold:")
        print("#" * 76)
        header = f"# {'Metric':20} | {'Magnitude':10} | {'Threshold':10} | {'Result':10} | {'Ratio':10} #"  # pylint: disable=line-too-long
        print(header)
        print("#" + "-" * (len(header) - 2) + "#")

        for metric, magnitude, ratio in self.not_passed:
            threshold = self.thresholds.get(metric, "N/A")
            result = self.results.get(metric + f"_{magnitude}", None)
            metric_str = (metric[:17] + "...") if len(metric) > 20 else metric
            line = f"# {metric_str:20} | {magnitude:<10.2f} | {threshold:<10.2f} | {result:<10.2f} | {ratio:<10.2f} #"  # pylint: disable=line-too-long
            print(line)

        print("#" * 76)

        veredict = self.norm_p(self.not_passed, 2)
        print(f"\nL2 Norm = {veredict:.2f} (max: {self.global_threshold:.2f})")

        if veredict > self.global_threshold:
            print("Recommendation: Review the change.\n")
        else:
            print("Change approved.\n")

    def _set_metrics_not_passed(self) -> None:
        """
        Set the metrics that did not pass the veredict.
        """
        results = self.get_global_results()
        for metric, result in results.items():
            magnitude = metric[-1:]
            metric = metric[:-2]
            threshold = self.thresholds[metric]
            if result > threshold:
                if threshold == 0:
                    ratio = 1  # ver
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
