import time


def fib(n: int) -> int:
    if n <= 1:
        return n
    else:
        return fib(n - 2) + fib(n - 1)


t0 = time.time()
fib(32)
print(time.time() - t0)
