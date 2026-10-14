import sys

raw_arguments = sys.argv[1:]

print(raw_arguments)
print(sys.argv)


class ArgumentDefinition:
    def __init__(self, *keys: str):
        self.keys = keys

    def matches(self):
        return any(key in sys.argv[1:] for key in self.keys)

    def matches_at(self) -> int:
        if self.matches():
            for key in self.keys:
                return sys.argv.index(key)
        raise Exception()

    @property
    def value(self) -> str:
        return sys.argv[self.matches_at() + 1]


if __name__ == "__main__":
    name = ArgumentDefinition("--name", "-n")
    # print(name.matches())
    # print(name.matches_at())
    value = name.value
    print(value)
