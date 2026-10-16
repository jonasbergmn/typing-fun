from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

T = TypeVar("T")


class ArgumentError(Exception):
    """Base exception for argument parsing errors."""


class ArgumentNotFoundError(ArgumentError):
    """Raised when a required argument is not found."""

    def __init__(self, *keys: str) -> None:
        self.keys = keys
        super().__init__(f"Did not find required argument: {', '.join(keys)}")


class MissingArgumentValueError(ArgumentError):
    """Raised when an argument flag is provided without a following value."""

    def __init__(self, key: str) -> None:
        super().__init__(f"Missing value for argument: {key}")


class ArgumentDefinition(Generic[T]):
    """Defines a parsable CLI argument."""

    def __init__(
        self,
        *keys: str,
        description: str = "",
        default: T | None = None,
        required: bool = False,
        converter: Callable[[str], T] = str,  # type: ignore[assignment]  # ty: ignore[invalid-parameter-default]
    ) -> None:
        if not keys:
            raise ValueError("At least one key (e.g., '--name') must be provided.")
        self.keys = keys
        self.description = description
        self.default = default
        self.required = required
        self.converter = converter
        self._value: T | None = default

    def parse_from(self, global_args: Sequence[str], known_flags: set[str]) -> None:
        """Extracts and converts the argument value from the CLI argument list."""
        for key in self.keys:
            if key in global_args:
                idx = global_args.index(key) + 1
                if idx >= len(global_args) or global_args[idx] in known_flags:
                    raise MissingArgumentValueError(key)

                raw_val = global_args[idx]
                try:
                    self._value = self.converter(raw_val)
                except ValueError as err:
                    raise ArgumentError(
                        f"Invalid value '{raw_val}' for {key}: {err}"
                    ) from err
                return

        if self.required and self.default is None:
            raise ArgumentNotFoundError(*self.keys)

    @property
    def registry_item(self) -> dict[str, object]:
        return {
            "keys": list(self.keys),
            "description": self.description,
            "default": self.default,
            "required": self.required,
        }

    @property
    def value(self) -> T:
        if self._value is None:
            raise ArgumentError(
                f"Argument {self.keys} has not been resolved or has no value."
            )
        return self._value

    @value.setter
    def value(self, val: T) -> None:
        self._value = val


class ArgumentContext:
    """Context manager for registering and compiling CLI arguments."""

    def __init__(self, argv: Sequence[str] | None = None) -> None:
        self.args: list[ArgumentDefinition[object]] = []
        self._global_args: Sequence[str] = argv if argv is not None else sys.argv[1:]

    def __enter__(self) -> ArgumentContext:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        # Only compile if no exception occurred inside the `with` block
        if exc_type is None:
            self.compile()

    def add_argument(
        self,
        *keys: str,
        description: str = "",
        default: T | None = None,
        required: bool = False,
        converter: Callable[[str], T] = str,  # type: ignore[assignment]  # ty: ignore[invalid-parameter-default]
    ) -> ArgumentDefinition[T]:
        arg = ArgumentDefinition(
            *keys,
            description=description,
            default=default,
            required=required,
            converter=converter,
        )
        self.args.append(arg)
        return arg

    def compile(self) -> None:
        known_flags = {key for arg in self.args for key in arg.keys}
        for arg in self.args:
            arg.parse_from(self._global_args, known_flags)


if __name__ == "__main__":
    # You can pass a test list like ArgumentContext(["-n", "Alice", "-a", "25"])
    with ArgumentContext() as ctx:
        name_arg = ctx.add_argument(
            "--name",
            "-n",
            description="Your Name",
            default="Jonas",
        )
        age_arg = ctx.add_argument(
            "--age",
            "-a",
            description="Your age",
            default=31,
            converter=int,
        )

    print(f"Name: {name_arg.value} (type: {type(name_arg.value).__name__})")
    print(f"Age: {age_arg.value} (type: {type(age_arg.value).__name__})")
