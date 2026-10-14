from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from timeseries.constants import FORMAT
from timeseries.type_definitions import Number, Points

if TYPE_CHECKING:
    from datetime import datetime

    from timeseries.grid import Grid


class IncompatibelGridException(Exception): ...


@dataclass
class TimeSeries:
    points: Points = field(default_factory=dict)

    @staticmethod
    def make_timeseries(grid: "Grid", default: Number = 0) -> "TimeSeries":
        points = {k: default for k in grid.values}
        return TimeSeries(points=points)

    def repr(self):
        repr = ""
        for k, v in self.points.items():
            repr += str(k.strftime(FORMAT)) + " - " + str(v) + "\r\n"
        return repr

    def tail(self, n: int | None = 5):
        repr: list[tuple[datetime, Number]] = []
        for i, (k, v) in enumerate(self.points.items()):
            if n is not None and len(self.points) - n > i:
                continue
            repr.append((k, v))

        self._print_header()

        for k, v in repr:
            print(k.strftime(FORMAT), v)

    def head(self, n: int | None = 5):
        repr: list[tuple[datetime, Number]] = []
        for i, (k, v) in enumerate(self.points.items()):
            repr.append((k, v))
            if n is not None and i == n - 1:
                break

        self._print_header()

        for k, v in repr:
            print("|" + k.strftime(FORMAT) + " |", str(v) + " |")

    def _print_header(self):
        print("#############")

    def _guard_against_other(self, other: "TimeSeries"):
        if len(self.points) != len(other.points):
            raise IncompatibelGridException()

    def __repr__(self):
        return self.repr()

    def __add__(self, other: "TimeSeries") -> "TimeSeries":
        self._guard_against_other(other)

        kv: dict[datetime, Number] = {}
        for k in self.points:
            kv[k] = self.points[k] + other.points[k]

        return TimeSeries(points=kv)

    def __mul__(self, other: "TimeSeries") -> "TimeSeries":
        self._guard_against_other(other)

        kv: dict[datetime, Number] = {}
        for k in self.points:
            kv[k] = self.points[k] * other.points[k]

        return TimeSeries(points=kv)
