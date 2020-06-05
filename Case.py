class Case:
    def __init__(self, pos, worldSize, mucus=False):
        self.position = pos
        self._value = 0

        line = pos // worldSize[1]
        col = pos % worldSize[1]
        self.Coord = (line, col)

        self.agents = []
        self.mucus = mucus

    def __repr__(self):
        return str(self.position)

    def setField(self, value):
        self._value += value

    def getField(self):
        return self._value

    def resetField(self):
        self._value = 0

    def isIn(self, typeList):
        for t in typeList:
            unType = False
            for a in self.agents:
                if type(a) == t: unType = True

            if not unType: return False

        return True
