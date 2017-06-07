from memory_profiler import profile
@profile
def foo():
    sum = 0
    for i in range(10000):
        sum += i
    return sum
if __name__=="__main__":
    try :
        import profile as cProfile
    except:
        import cProfile 
        
    cProfile.run("foo()","foo.txt")
    import pstats
    p = pstats.Stats("foo.txt")
    p.sort_stats("time").print_stats()