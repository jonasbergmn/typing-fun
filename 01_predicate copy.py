from typing import Callable, Annotated
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Customer:
    name: Annotated[str, "This is the name of the Customer"]

    def __gt__(self, predicate: 'Predicate[Customer]') -> bool:
        return predicate(self)

class PredicateChain[T]:
    def __init__(self):
        self.predicates: list[Predicate[T]] = []

    def add(self, predicate: 'Predicate[T]') -> None:
        self.predicates.append(predicate)

    def __add__(self, predicate: 'Predicate[T]') -> 'PredicateChain[T]':
        self.predicates.append(predicate)
        return self

    def __call__(self, subject: T) -> bool:
        print(f"Subject: {subject}")
        res = all([i(subject) for i in self.predicates])
        print(f"Result: {res}")
        return res


class Predicate[T]:
    def __init__(self, func: Callable[[T], bool], descr: str):
        self.func: Callable[[T], bool] = func
        self.descr = descr

    def __call__(self, subject: T) -> bool:
        res = self.func(subject)
        print(f"{self.descr}: {res}")
        return res

    def __add__(self, other: 'Predicate[T]') -> PredicateChain[T]:
        chain = PredicateChain[T]()
        chain.add(self)
        chain.add(other)
        return chain



p1 = Predicate[Customer](lambda x: len(x.name) > 1, "Longer than 1")
p2 = Predicate[Customer](lambda x: x.name.lower().startswith("j"), "Starts with j")
p3 = Predicate[Customer](lambda x: x.name.lower().endswith("s"), "Ends with s")

c = Customer("jonas")

p3 = p1 + p2 + p3

p3(c)