from typing import Callable, Sequence, overload

type Number = int | float
type NullableNumber = Number | None


a: Number = 1
b: NullableNumber = 2
c: NullableNumber = None
d: Number = 1.1


class Aggregator:
    def __init__(
        self,
        func: Callable[..., NullableNumber],
    ):
        self._func = func

    @overload
    def __call__(self, numbers: Sequence[Number]) -> Number: ...

    @overload
    def __call__(self, numbers: Sequence[NullableNumber]) -> NullableNumber: ...

    def __call__(
        self, numbers: Sequence[Number] | Sequence[NullableNumber]
    ) -> NullableNumber:
        nums = [number for number in numbers if number is not None]
        return self._func(nums) if nums else None


def avg(numbers: Sequence[NullableNumber]) -> NullableNumber:
    not_nones = [i for i in numbers if i is not None]
    if not_nones:
        return sum(not_nones) / len(not_nones)
    return None


max_aggregator = Aggregator(max)
min_aggregator = Aggregator(min)
avg_aggregator = Aggregator(avg)
sum_aggregator = Aggregator(sum)

numbers = (1, 2, 3, 4)

max_res = max_aggregator(numbers)
min_res = min_aggregator(numbers)
avg_res = avg_aggregator(numbers)
sum_res = sum_aggregator(numbers)

print(max_res)
print(min_res)
print(avg_res)
print(sum_res)

numbers: Sequence[NullableNumber] = (1, 2, 3, 4, None)

max_res = max_aggregator(numbers)
min_res = min_aggregator(numbers)
avg_res = avg_aggregator(numbers)
sum_res = sum_aggregator(numbers)

print(max_res)
print(min_res)
print(avg_res)
print(sum_res)

numbers: Sequence[NullableNumber] = (None, None)

max_res = max_aggregator(numbers)
min_res = min_aggregator(numbers)
avg_res = avg_aggregator(numbers)
sum_res = sum_aggregator(numbers)

print(max_res)
print(min_res)
print(avg_res)
print(sum_res)
