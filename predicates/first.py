from collections.abc import Callable


class Predicate[T]:
    def __init__(self, func: Callable[[T], bool], descr: str):
        self.func: Callable[[T], bool] = func
        self.descr = descr

    def __call__(self, subject: T) -> bool:
        res = self.func(subject)
        print(f"{self.descr}: {res} {'✅' if res else '❌'}")
        return res

    def __add__(self, other: "Predicate[T]") -> "PredicateChain[T]":
        chain = PredicateChain[T](self, other)
        return chain


class PredicateChain[T]:
    def __init__(self, *args: Predicate[T]):
        self.predicates: list[Predicate[T]] = []
        for predicate in args:
            self.predicates.append(predicate)

    def add(self, predicate: Predicate[T]) -> None:
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
