import argparse
from typing import TypeVar

_ARG_TYPES = str | int | float


class AargParser:
    def __init__(self): ...

    def __enter__(self) -> "AargParser": ...

    def add_arg[T: _ARG_TYPES](self, arg_keys: str, t: TypeVar): ...

    def __exit__(self, type, value, traceback): ...


def demo():
    with AargParser() as aarg:
        aarg.add_arg("demo", t=str)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--name",
        "-n",
        type=str,
        default="Jonas",
        help="Tell me your name",
    )

    args = arg_parser.parse_args()

    print(args.name)
