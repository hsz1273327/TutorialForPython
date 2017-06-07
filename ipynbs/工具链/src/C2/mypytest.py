
from typing import Callable

def twice(i: int, next: Callable[[int], int]) -> int:
    return next(next(i))

def add(i: int) -> str:#写成返回str,这样就会报错!
    return i + 1

print(twice(3, add))   # 5