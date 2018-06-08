#cython: language_level=3
from math import exp


cpdef double logistic(double x):
    return 1/(1+exp(-x))