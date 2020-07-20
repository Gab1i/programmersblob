class Veine:
    def __init__(self, blob, parent=None, sexe=0):
        self.Parent = parent
        self.Children = []
        self._max = 10
        self._growingRate = 1
        self._dessication = False
        self._dead = False
        self._sexe = sexe
        self._blob = blob

        if self.Parent is not None:
            self.Parent.Children.append(self)

    @property
    def isExtremity(self):
        return len(self.Children) == 0 or (self.Parent is None and len(self.Children) == 1)

    def Grow(self):
        self._size = min(self._size + self._growingRate, self._max)

    def Shrink(self):
        self._size = self._size - self._growingRate * 2

    def Kill(self):
        if self.Parent is not None:
            try:
                self.Parent.Children.remove(self)
            except:
                pass

        for child in self.Children:
            child.Parent = None
