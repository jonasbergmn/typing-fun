import sys


class ArgumentNotFoundError(Exception):
    """Is raised when an argument is not found."""

    def __init__(self, *keys: str):
        self._keys = keys
        self.msg = f"Did not find argument {','.join(self._keys)}"
        super().__init__(self.msg)


class ArgumentDefinition:
    """Defines an Argument Definition. Use this to define new parsable Arguments."""

    def __init__(
        self,
        *keys: str,
        description: str | None = None,
        default: object = None,
    ) -> None:
        """Initializes the Argument Definition with the keys it listens to, a descriptions and a default value.

        Make sure to use kwargs only.
        """
        self.keys = keys
        self.description = description
        self.default = default
        self._value: str | None = None

    def guard(self, global_args: list[str]) -> None:
        if not any(key in global_args for key in self.keys):
            raise ArgumentNotFoundError(*self.keys)

    def matches_at(self, global_args: list[str]) -> int:
        self.guard(global_args)
        for key in self.keys:
            return global_args.index(key) + 1
        raise ArgumentNotFoundError(*self.keys)

    @property
    def registry_item(self):
        return {
            "keys": list(self.keys),
            "description": self.description or "",
            "default": self.default,
        }

    def set_value(self, value: str) -> None:
        self._value = value

    @property
    def value(self) -> str:
        if self._value is None:
            raise Exception
        return self._value


class ArgumentContext:
    def __init__(self):
        self.args: list[ArgumentDefinition] = []
        self._global_args: list[str] = sys.argv[1:]

    def __enter__(self) -> ArgumentContext:
        return self

    def __exit__(self, a, b, c):
        self.compile()

    def add_argument(
        self,
        *keys: str,
        description: str | None = None,
        default: object = None,
    ) -> ArgumentDefinition:
        arg = ArgumentDefinition(*keys, description=description, default=default)
        self.args.append(arg)
        return arg

    def compile(self) -> None:
        for arg in self.args:
            arg.guard(self._global_args)
            try:
                value = self._global_args[arg.matches_at(self._global_args)]
            except:
                raise Exception("No value for arg")
            arg.set_value(value)


if __name__ == "__main__":
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
            default="31",
        )
    print(name_arg.value, age_arg.value)
