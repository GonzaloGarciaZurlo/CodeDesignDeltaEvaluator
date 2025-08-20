"""
This module contains functions for handling derived metrics.
"""
from overrides import override
from src.cdde.expr_evaluator import ExprEvaluator, MetricType
from src.cdde.addons_api import CddeAPI
from typing import Optional
import pysqlite3 as sqlite3
from enum import StrEnum


class TableName(StrEnum):
    CLASSES = "classes"
    PACKAGES = "packages"


class AggregatedMetrics(ExprEvaluator):
    """
    This class is responsible for calculating the aggregated metrics.
    """

    def __init__(self):
        self._api = None
        self._db = None
        self._db_cursor = None

    @override
    def eval(self,
             expr: str,
             arguments: dict[str, str],    # type: ignore
             results: dict[str, str | float]) -> MetricType:   # type: ignore
        """
        Evaluate an expression.
        """
        self._api = results
        if not self._db:
            self._set_db()

    def _set_db(self) -> None:
        self._db = sqlite3.connect("table.db")
        self._db_cursor = self._db.cursor()
        d1, d2 = self.split_dict(self._api, "___SEP___nodes", include=False)

        metrics_classes_names, classes = self._get_metrics_names_and_types(d1)
        self._create_db(metrics_classes_names, TableName.CLASSES)
        self._populate_tables(metrics_classes_names,
                              classes, TableName.CLASSES)

        metrics_packages_names, packages = self._get_metrics_names_and_types(d2)
        self._create_db(metrics_packages_names, TableName.PACKAGES)
        self._populate_tables(metrics_packages_names,
                              packages, TableName.PACKAGES)

    def split_dict(self, data: dict, cut_suffix: str, include=True):
        items = list(data.items())

        for i, (k, v) in enumerate(items):
            if k.endswith(cut_suffix):
                if include:
                    return dict(items[:i+1]), dict(items[i+1:])
                else:
                    return dict(items[:i]), dict(items[i:])
        
        return data, {}


    def _get_metrics_names_and_types(self, api: dict[str, str | float]) -> tuple[list[str], list[str]]:
        """
        Get the names of the metrics.
        """
        names = []
        types = []
        for name, result in api.items():
            if isinstance(result, (int, float)) and "___SEP___" in name:
                metric_name = name.split("___SEP___")[1]
                types_name = name.split("___SEP___")[0]

                if metric_name not in names:
                    names.append(metric_name)
                if types_name not in types:
                    types.append(types_name)
        return names, types

    def _get_metric_result(self, time: str, metric_name: str, type_name: str) -> Optional[int | float]:
        metric = time + type_name + "___SEP___" + metric_name
        return self._api.get(metric, "NULL")

    def _create_db(self, metrics_names: list[str], table: TableName) -> None:
        sqlQuery = f"""
        CREATE TABLE "{table}" (
        "time" TEXT NOT NULL,
        "name" TEXT NOT NULL,
        {', '.join(f'"{name}" REAL' for name in metrics_names)}
        );"""
        self._db_cursor.execute(sqlQuery)
        self._db.commit()

    def _populate_tables(self, metrics_names: list[str], types: list[str], table: TableName) -> None:
        for type in types:
            if 'before' in type:
                time = 'before'
                type = type.removeprefix('before')
            else:
                time = 'after'
                type = type.removeprefix('after')

            sqlQuery = f"""
            INSERT INTO {table} (time, name, {', '.join(metrics_names)}) VALUES ("{time}", "{type}", {', '.join(str(self._get_metric_result(time, name, type)) for name in metrics_names)})
            """
            self._db_cursor.execute(sqlQuery)
            self._db.commit()


def init_module(api: CddeAPI) -> None:
    """
    Initializes the module on the API.
    """
    api.register_expr_evaluator('aggregated-metrics', AggregatedMetrics)
