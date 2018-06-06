from memory_profiler import profile
@profile
def foo():
    sum = 0
    for i in range(10000):
        sum += i
    return sum
if __name__=="__main__":
    foo()