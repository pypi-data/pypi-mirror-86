from FrameNet.LexicalUnit cimport LexicalUnit


cdef class Frame:

    cdef str name
    cdef list lexicalUnits

    cpdef bint lexicalUnitExists(self, str synSetId)
    cpdef LexicalUnit getLexicalUnitWithId(self, str synSetId)
    cpdef removeLexicalUnit(self, str synSetId)
    cpdef LexicalUnit getLexicalUnit(self, int index)
    cpdef int size(self)
    cpdef str getName(self)
