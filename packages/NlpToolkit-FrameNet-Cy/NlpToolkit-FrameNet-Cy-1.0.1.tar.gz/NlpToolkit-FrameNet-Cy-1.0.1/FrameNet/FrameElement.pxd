cdef class FrameElement(object):

    cdef str __frameElementType
    cdef str __id

    cpdef initWithId(self, str frameElementType, str _id)
    cpdef str getFrameElementType(self)
    cpdef str getId(self)
