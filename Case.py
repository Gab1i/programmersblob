class Case:
    def __init__(self, pos, worldSize, mucus=False):
        self.position = pos
        self._value = 0

        line = pos // worldSize[1]
        col = pos % worldSize[1]
        self.Coord = (line, col)

        self.Veine = None

        self.agents = []
        self.mucus = mucus

        self.child = 0
        self.children = []
        self.parent = None
        self.Spores = []
        self.Sel = True


    def setParent(self, parent):
        self.parent = parent
        if self.parent is not None:
            self.parent.child += 1
            # CACA ICI
            parent.children.append(self)

    @property
    def isExtremity(self):
        return self.child == 0 or self.parent is None

    def __repr__(self):
        return "Case {0} ... children : {1}".format(self.position, self.child)

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



    def TimeToKen(self):
        spores = []
        if len(self.Spores) > 1:
            sexe = self.Spores[0]._sexe
            spores.append(self.Spores[0])
            for i in range(1, len(self.Spores)):
                if sexe != self.Spores[i]._sexe:
                    spores.append(self.Spores[i])
                    return spores

        return []

    def AddSpore(self, spore):
        self.Spores.append(spore)

    def RemoveSpore(self, spore):
        self.Spores.remove(spore)