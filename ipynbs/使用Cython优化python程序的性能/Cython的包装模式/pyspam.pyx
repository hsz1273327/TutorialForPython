
cdef extern from "spam.c":
    int order_spam(int tons)

cpdef pyorder_spam(int tons):
    return order_spam(tons)