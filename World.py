# -*- coding: utf-8 -*-

from Case import Case


class World:
    """
        class used to manage the simulation
    """

    def __init__(self, size):
        """
        :param size: square size of the world
        """
        self.size = size
        self.grid = [Case() for i in range(size * size)]
        self.agents = []

    def pos2coord(self, pos):
        """
        Convert position to coordinates
        :param pos: A position in the world
        :return: (line, col) corresponding to the given position
        """
        line = pos // self.size
        col = pos % self.size
        return (line, col)

    def coord2pos(self, line, col):
        """
        Convert coordinate to position
        :param line:
        :param col:
        :return: the position corresponding to the given coordinates
        """
        return int(line * self.size + col)

    def setField(self):
        """
        Compute the field emmited by each agent on the grid
        """
        for agent in self.agents:
            for key, e in agent.emetteurs.items():
                d = e.power / e.decay

                for i in range(int(d)):
                    (line, col) = agent.coord
                    neighbors = self.neighbor(line, col, i)
                    for n in neighbors:
                        self.grid[n].updateField(e.name, e.power - e.decay * i)

    def neighbor(self, line, col, n):
        """
        Look for the neighbors at a given distance (Moore neighborhood)
        :param line:
        :param col:
        :param n: The distance to look for neighbors
        :return: a list of positions corresponding to the neighbors
        """
        l = []
        for y in range(int(col - n), int(col + n + 1)):
            p = self.coord2pos(line - n, y)
            if 0 < p < self.size ** 2: l.append(p)
            p = self.coord2pos(line + n, y)
            if 0 < p < self.size ** 2: l.append(p)

        for x in range(int(line - n + 1), int(line + n)):
            p = self.coord2pos(x, col + n)
            if 0 < p < self.size ** 2: l.append(p)
            p = self.coord2pos(x, col - n)
            if 0 < p < self.size ** 2: l.append(p)

        return set(l)

    def birthControl(self):
        pass

    def sarahConnor(self):
        pass

    def tick(self):
        self.setField()
        self.sarahConnor()
        self.birthControl()

    def run(self, loop):
        for i in range(loop):
            self.tick()
