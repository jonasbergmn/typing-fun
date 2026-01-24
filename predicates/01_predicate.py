from typing import Callable, Annotated
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Customer:
    name: Annotated[str, "This is the name of the Customer"]

    def __gt__(
        self, predicate: "Predicate[Customer] | PredicateChain[Customer]"
    ) -> bool:
        return predicate(self)


class PredicateChain[T]:
    def __init__(self, *args: "Predicate[T]"):
        self.predicates: list[Predicate[T]] = []
        for predicate in args:
            self.predicates.append(predicate)

    def add(self, predicate: "Predicate[T]") -> None:
        self.predicates.append(predicate)

    def __add__(
        self,
        predicate: "Predicate[T] | PredicateChain[T]",
    ) -> "PredicateChain[T]":
        match predicate:
            case PredicateChain():
                for p in predicate.predicates:
                    self.predicates.append(p)
                return self
            case Predicate():
                self.predicates.append(predicate)
                return self

    def __call__(self, subject: T) -> bool:
        print(40 * "#")
        print(f"Subject: {subject}")
        res = all([i(subject) for i in self.predicates])
        print(f" ---> Result: {res}")
        print(40 * "#")
        return res


class Predicate[T]:
    def __init__(self, func: Callable[[T], bool], descr: str):
        self.func: Callable[[T], bool] = func
        self.descr = descr

    def __call__(self, subject: T) -> bool:
        res = self.func(subject)
        print(f"{self.descr}: {res} {'✅' if res else '❌'}")
        return res

    def __add__(self, other: "Predicate[T]") -> PredicateChain[T]:
        chain = PredicateChain[T](self, other)
        return chain


p1 = Predicate[Customer](lambda x: len(x.name) > 1, "Longer than 1")
p2 = Predicate[Customer](lambda x: x.name.lower().startswith("j"), "Starts with j")
p3 = Predicate[Customer](lambda x: x.name.lower().endswith("s"), "Ends with s")
p4 = Predicate[Customer](lambda x: x.name.strip() != "", "Is not empty")
p5 = Predicate[Customer](lambda x: "a" in x.name, "Contains a")

c = Customer("jones")

pc1 = p1 + p2
pc2 = p3 + p4 + p5

pc3 = pc1 + pc2

result = pc3(c)
