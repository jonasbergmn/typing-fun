import sys
from typing import TypedDict

_args: list[RegisteredArg] = []


class RegisteredArg(TypedDict):
    keys: list[str]
    description: str
    default: object | None


class ArgumentNotFoundError(Exception):
    """Is raised when an argument is not found."""


class ArgumentDefinition:
    def __init__(
        self, *keys: str, description: str | None = None, default: object = None
    ) -> None:
        self.keys = keys
        _args.append(
            {"keys": list(keys), "description": description or "", "default": default}
        )

    def matches(self):
        return any(key in sys.argv[1:] for key in self.keys)

    def matches_at(self) -> int:
        if self.matches():
            for key in self.keys:
                return sys.argv.index(key)
        raise ArgumentNotFoundError

    @property
    def value(self) -> str:
        return sys.argv[self.matches_at() + 1]


if __name__ == "__main__":
    name_arg = ArgumentDefinition(
        "--name", "-n", description="Your Name", default="Jonas"
    )
    age_arg = ArgumentDefinition("--age", "-a", description="Your age", default=31)

    print(_args)
