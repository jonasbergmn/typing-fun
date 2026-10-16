from __future__ import annotations

import sys
from collections.abc import Sequence
from dataclasses import MISSING, dataclass, field, fields
from typing import Any, Self, TypeVar, get_type_hints

T = TypeVar("T", bound="CLIArgs")


def arg(
    *keys: str,
    description: str = "",
    default: Any = MISSING,
) -> Any:
    """Helper that wraps dataclasses.field to store CLI flag metadata."""
    metadata = {"keys": keys, "description": description}
    if default is not MISSING:
        return field(default=default, metadata=metadata)
    return field(metadata=metadata)


@dataclass
class CLIArgs:
    """Base class that turns any dataclass into a type-safe CLI parser."""

    @classmethod
    def parse(cls, argv: Sequence[str] | None = None) -> Self:
        raw_args = argv if argv is not None else sys.argv[1:]
        type_hints = get_type_hints(cls)
        parsed_kwargs: dict[str, Any] = {}

        # Gather all valid flags across all fields to prevent flag-eating
        all_flags = {
            k
            for f in fields(cls)
            for k in (f.metadata.get("keys") or (f"--{f.name.replace('_', '-')}",))
        }

        for f in fields(cls):
            # Default to "--field-name" if no explicit keys were provided
            keys = f.metadata.get("keys") or (f"--{f.name.replace('_', '-')}",)
            converter = type_hints.get(f.name, str)

            for key in keys:
                if key in raw_args:
                    idx = raw_args.index(key) + 1
                    if idx >= len(raw_args) or raw_args[idx] in all_flags:
                        raise ValueError(f"Missing value for argument: {key}")
                    try:
                        parsed_kwargs[f.name] = converter(raw_args[idx])
                    except ValueError as err:
                        raise ValueError(
                            f"Invalid value '{raw_args[idx]}' for {key}: expected {converter.__name__}"
                        ) from err
                    break
            else:
                # Key wasn't passed on CLI; check if it's required
                if f.default is MISSING and f.default_factory is MISSING:
                    raise ValueError(
                        f"Did not find required argument: {', '.join(keys)}"
                    )

        return cls(**parsed_kwargs)


# --- Usage ---


@dataclass
class AppConfig(CLIArgs):
    name: str = arg("--name", "-n", description="Your Name", default="Jonas")
    age: int = arg("--age", "-a", description="Your age", default=31)


if __name__ == "__main__":
    # Parse CLI arguments directly into a strongly-typed object
    config = AppConfig.parse(["-n", "Alice", "--age", "28"])

    # Direct attribute access (no .value needed!)
    print(f"Name: {config.name} (type: {type(config.name).__name__})")
    print(f"Age: {config.age} (type: {type(config.age).__name__})")
