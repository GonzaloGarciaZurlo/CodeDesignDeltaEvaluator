"""
This module contains functions for handling derived metrics.
"""
from typing import Optional
from enum import StrEnum
import os
import pysqlite3 as sqlite3  # type: ignore[import-untyped]
from overrides import override

from src.cdde.expr_evaluator import ExprEvaluator, MetricType
from src.cdde.addons_api import CddeAPI


class TableName(StrEnum):
    """
    Table names for the database."""
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
             arguments: dict[str, str],
             results: dict[str, str | float]) -> MetricType:
        """
        Evaluate an expression in sqlite.
        """
        self._api = results

        if not self._db:
            self._set_db()

        results = self.execute_sqlite(expr)
        return results  # type: ignore[return-value]

    # type: ignore[type-arg]
    def execute_sqlite(self, expr: str) -> dict[MetricType]:
        """
        Execute an expression in sqlite."""
        try:
            self._db_cursor.execute(expr)
            result = self._db_cursor.fetchone()
            if result:

                return {k: v for k, v in zip( # pylint: disable=unnecessary-comprehension
                    self._db_cursor.description, result)}
            return {}
        except:
            return 0

    def _set_db(self) -> None:
        self.delete_db()
        self._db = sqlite3.connect("table.db")  # pylint: disable=no-member
        self._db.enable_load_extension(True)
        self._db.load_extension("src/addons/extension-functions.so")
        self._db_cursor = self._db.cursor()
        d1, d2 = self.split_dict(self._api, "___SEP___nodes", include=False)

        metrics_classes_names, classes = self._get_metrics_names_and_types(d1)
        self._create_db(metrics_classes_names, TableName.CLASSES)
        self._populate_tables(metrics_classes_names,
                              classes, TableName.CLASSES)

        metrics_packages_names, packages = self._get_metrics_names_and_types(
            d2)
        self._create_db(metrics_packages_names, TableName.PACKAGES)
        self._populate_tables(metrics_packages_names,
                              packages, TableName.PACKAGES)

    def split_dict(self, data: dict, cut_suffix: str, include=True):
        """
        Split a dictionary into two dictionaries at
        the first occurrence of a key ending with cut_suffix.
        """
        items = list(data.items())

        for i, (k, _v) in enumerate(items):
            if k.endswith(cut_suffix):
                if include:
                    return dict(items[:i+1]), dict(items[i+1:])
                return dict(items[:i]), dict(items[i:])

        return data, {}

    def _get_metrics_names_and_types(self, api: dict[str, str | float]) -> tuple[
            list[str], list[str]]:
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

    def _get_metric_result(self, time: str, metric_name: str, type_name: str) -> Optional[
            int | float]:
        metric = time + type_name + "___SEP___" + metric_name
        return self._api.get(metric, "NULL")

    def _create_db(self, metrics_names: list[str], table: TableName) -> None:
        base_columns = ['"time" TEXT NOT NULL', '"name" TEXT NOT NULL']
        metric_columns = [f'"{name}" REAL' for name in metrics_names]
        all_columns = base_columns + metric_columns

        sql_query = f"""
        CREATE TABLE "{table}" (
            {', '.join(all_columns)}
        );"""
        self._db_cursor.execute(sql_query)
        self._db.commit()

    def _populate_tables(self, metrics_names: list[str], types: list[str],
                         table: TableName) -> None:
        for _type in types:
            if 'before' in _type:
                time = 'before'
                _type = _type.removeprefix('before')
            else:
                time = 'after'
                _type = _type.removeprefix('after')

            sql_query = f"""
            INSERT INTO {table} (time, name, {', '.join(metrics_names)})
              VALUES ("{time}","{_type}",
                {', '.join(str(self._get_metric_result(time, name, _type))
                           for name in metrics_names)})
            """
            self._db_cursor.execute(sql_query)
            self._db.commit()

    def delete_db(self) -> None:
        """
        Delete the database.
        """
        if os.path.exists("table.db"):
            os.remove("table.db")


def init_module(api: CddeAPI) -> None:
    """
    Initializes the module on the API.
    """
    api.register_expr_evaluator('aggregated-metrics', AggregatedMetrics)
