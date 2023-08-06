import os
import xml.etree.ElementTree


cdef class FrameNet:

    def __init__(self, directory="../Frames/"):
        self.frames = []
        for r, d, f in os.walk(directory):
            for file in f:
                if file.endswith(".xml"):
                    root = xml.etree.ElementTree.parse(os.path.join(r, file)).getroot()
                    self.frames.append(Frame(file, root))

    cpdef bint lexicalUnitExists(self, str synSetId):
        cdef Frame frame
        for frame in self.frames:
            if frame.lexicalUnitExists(synSetId):
                return True
        return False

    cpdef list getFrames(self, str synSetId):
        cdef list result
        cdef Frame frame
        result = []
        for frame in self.frames:
            if frame.lexicalUnitExists(synSetId):
                result.append(frame)
        return result

    cpdef int size(self):
        return len(self.frames)

    cpdef Frame getFrame(self, int index):
        return self.frames[index]
