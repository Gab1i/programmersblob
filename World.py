from Blob import Blob
from Case import *

class World:
    def __init__(self, line, col, pos):
        self.line = line
        self.col = col
        self.grid = [ Case(i, (line, col)) for i in range(line * col) ]

        self._blob = Blob(self, pos)
        self._emitters = []
        #self.AddAgent(self._blob, pos)

    def Neighborhood(self, case, n=1):
        """
        Look for the neighbors at a given distance (Moore neighborhood)
        :param line:
        :param col:
        :param n: The distance to look for neighbors
        :return: a list of positions corresponding to the neighbors
        """
        line, col = case.Coord

        l = []
        for y in range(int(col - n), int(col + n + 1)):
            if line - n >= 0 and 0 <= y < self.col:
                p = self.coord2pos(line - n, y)
                l.append(self.grid[p])

            if line + n < self.line and 0 <= y < self.col:
                p = self.coord2pos(line + n, y)
                l.append(self.grid[p])

        for x in range(int(line - n + 1), int(line + n)):
            if col - n >= 0 and 0 <= x < self.line:
                p = self.coord2pos(x, col - n)
                l.append(self.grid[p])

            if col + n < self.col and 0 <= x < self.line:
                p = self.coord2pos(x, col + n)
                l.append(self.grid[p])

        return set(l)

    def pos2coord(self, pos):
        """
        Convert position to coordinates
        :param pos: A position in the world
        :return: (line, col) corresponding to the given position
        """
        line = pos // self.col
        col = pos % self.col
        return line, col

    def coord2pos(self, line, col):
        """
        Convert coordinate to position
        :param line:
        :param col:
        :return: the position corresponding to the given coordinates
        """
        return int(line * self.col + col)

    def AddEmitter(self, agent, p):
        self.grid[p].agents.append(agent)
        self._emitters.append(agent)

    def DeleteAgent(self, agent, p):
        self._emitters.remove(agent)
        self.grid[p].agents.remove(agent)

    def Tick(self):
        self.ComputeField()

        self._blob.Feed()

        self._blob.Kill()
        self._blob.Add()
        self._blob.Add()
        #self._blob.Grow()
        #print(self._blob._cases)

    def ComputeField(self):
        """
        Compute the field emitted by each agent on the grid
        """
        self.resetFields()

        for e in self._emitters:
            d = e.decay

            for i in range(abs(d)):
                neighbors = self.Neighborhood(self.grid[e.pos], i)

                for n in neighbors:
                    n.setField(e.power + ((e.power/e.decay) * i))
                    print(e.power + ((e.power/e.decay) * i))

    def resetFields(self):
        for c in self.grid:
            c.resetField()
