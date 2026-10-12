from dataclasses import dataclass
from typing import Annotated

from predicates.first import Predicate, PredicateChain


@dataclass(slots=True, frozen=True)
class Customer:
    name: Annotated[str, "This is the name of the Customer"]

    def __gt__(
        self, predicate: "Predicate[Customer] | PredicateChain[Customer]"
    ) -> bool:
        return predicate(self)


def test_predicate_init():
    p = Predicate[Customer](lambda x: "J" in x.name, "Contains a 'J'")
    assert p(Customer("Jonas"))


def test_predicate_combine():
    p1 = Predicate[Customer](lambda x: "J" in x.name, "Contains a 'J'")
    p2 = Predicate[Customer](lambda x: "o" in x.name, "Contains a 'o'")

    p12 = p1 + p2

    assert type(p12) is PredicateChain
    assert p12(Customer("Jonas"))
