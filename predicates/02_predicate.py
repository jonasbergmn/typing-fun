from typing import Callable, Annotated
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Customer:
    name: Annotated[str, "This is the name of the Customer"]

    def __gt__(self, predicate: 'Predicate[Customer]') -> bool:
        return predicate(self)


class Predicate[T]:
    def __init__(self, func: Callable[[T], bool], descr: str):
        self.func: Callable[[T], bool] = func
        self.descr = descr

    def __call__(self, subject: T) -> bool:
        print(self)
        return self.func(subject)

    def combine(self, other: 'Predicate[T]'):
        return Predicate[T](
            lambda x : self.func(x) and other.func(x),
            "\r\n".join((self.descr, other.descr)))

    def __add__(self, other: 'Predicate[T]'):
        return self.combine(other)

    def __repr__(self) -> str:
        return self.descr

    def __or__(self, value: T) -> bool:
        return self.func(value)


p1 = Predicate[Customer](lambda x: len(x.name) > 1, "Longer than 1")
p2 = Predicate[Customer](lambda x: x.name.lower().startswith("j"), "Starts with j")
p3 = Predicate[Customer](lambda x: x.name.lower().endswith("s"), "Ends with s")

c = Customer("jona")

result = c > p1 + p2 + p3
result = (p1 + p2 + p3)(c) # same like row above
