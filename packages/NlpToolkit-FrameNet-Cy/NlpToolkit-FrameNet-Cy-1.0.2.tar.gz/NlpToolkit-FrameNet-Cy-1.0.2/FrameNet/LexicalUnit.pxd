cdef class LexicalUnit:

    cdef str synSetId
    cdef list frameElements

    cpdef str getSynSetId(self)
    cpdef int size(self)
    cpdef list getFrameElements(self)
