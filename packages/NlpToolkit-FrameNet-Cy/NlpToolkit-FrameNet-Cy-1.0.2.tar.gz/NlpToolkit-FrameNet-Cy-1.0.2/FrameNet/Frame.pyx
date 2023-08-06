from xml.dom.minidom import Element


cdef class Frame:

    def __init__(self, name: str, root: Element):
        self.lexicalUnits = []
        self.name = name
        for lexicalUnit in root:
            self.lexicalUnits.append(LexicalUnit(lexicalUnit.attrib["ID"], lexicalUnit))

    cpdef bint lexicalUnitExists(self, str synSetId):
        cdef LexicalUnit lexicalUnit
        for lexicalUnit in self.lexicalUnits:
            if lexicalUnit.getSynSetId() == synSetId:
                return True
        return False

    cpdef LexicalUnit getLexicalUnitWithId(self, str synSetId):
        cdef LexicalUnit lexicalUnit
        for lexicalUnit in self.lexicalUnits:
            if lexicalUnit.getSynSetId() == synSetId:
                return lexicalUnit
        return None

    cpdef removeLexicalUnit(self, str synSetId):
        cdef LexicalUnit lexicalUnit
        for lexicalUnit in self.lexicalUnits:
            if lexicalUnit.getSynSetId() == synSetId:
                self.lexicalUnits.remove(lexicalUnit)
                break

    cpdef LexicalUnit getLexicalUnit(self, int index):
        return self.lexicalUnits[index]

    cpdef int size(self):
        return len(self.lexicalUnits)

    cpdef str getName(self):
        return self.name
