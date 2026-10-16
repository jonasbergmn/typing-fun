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
    def help(cls, raw_args: Sequence[str]) -> bool:
        return bool("--help" in raw_args or "-h" in raw_args)

    @classmethod
    def render_help(cls) -> None:
        rows = [
            (
                f"Keys=[{','.join(f.metadata['keys'])}]",
                f"desc={f.metadata['description']}",
                f"default={f.default}",
                f"type={f.type}",
            )
            for f in fields(cls)
        ]

        if not rows:
            return

        # Calculate the maximum width of the first two columns
        w_keys = max(len(r[0]) for r in rows)
        w_desc = max(len(r[1]) for r in rows)
        w_def = max(len(r[2]) for r in rows)

        # Print with left-alignment (<) and a 4-space gap between columns
        for keys_str, desc_str, def_str, type_str in rows:
            print(
                f"{keys_str:<{w_keys}} {desc_str:<{w_desc}} {def_str:<{w_def}} {type_str}"
            )

    @classmethod
    def parse(cls, argv: Sequence[str] | None = None) -> Self:
        raw_args = argv if argv is not None else sys.argv[1:]
        type_hints = get_type_hints(cls)
        parsed_kwargs: dict[str, Any] = {}

        if cls.help(raw_args):
            cls.render_help()
            raise sys.exit(None)

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
    size: float = arg("--size", "-s", description="size", default=1.5)


if __name__ == "__main__":
    # Parse CLI arguments directly into a strongly-typed object
    config = AppConfig.parse()

    # Direct attribute access (no .value needed!)
    print(f"Name: {config.name} (type: {type(config.name).__name__})")
    print(f"Age: {config.age} (type: {type(config.age).__name__})")
    print(f"Age: {config.size} (type: {type(config.size).__name__})")
