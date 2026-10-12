from dataclasses import dataclass
from datetime import datetime, timedelta

from timeseries.constants import FORMAT


@dataclass
class Grid:
    values: list[datetime]

    @property
    def steps(self):
        return len(self.values)

    @staticmethod
    def make_grid(start: datetime, step_size: timedelta, steps: int) -> "Grid":
        values: list[datetime] = list()
        for i in range(steps):
            values.append(start + step_size * i)

        return Grid(values=values)

    def __repr__(self):
        return "".join([i.strftime(FORMAT) + "\r\n" for i in self.values])
