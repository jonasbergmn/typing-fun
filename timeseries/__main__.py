from datetime import UTC, datetime, timedelta

from timeseries.grid import Grid
from timeseries.timeseries import TimeSeries

if __name__ == "__main__":
    start = datetime(2026, 1, 1, 0, 0, tzinfo=UTC)
    step_size = timedelta(minutes=15)
    steps = 96
    g = Grid.make_grid(start, step_size, steps)

    t1 = TimeSeries.make_timeseries(grid=g, default=0)
    t2 = TimeSeries.make_timeseries(grid=g, default=5)
    t3 = TimeSeries.make_timeseries(grid=g, default=3)

    t4 = t1 + t2
    t5 = t2 * t3 * t3 * t2 * t3

    t4.head(n=5)
    t5.head(n=5)
