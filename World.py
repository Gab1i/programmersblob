# -*- coding: utf-8 -*-
from Agent import *
from Case import Case
from random import randint


class World:
    """
        TODO: Trouver une solution pour éviter les séparations
        TODO: Bouffe
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
        self.resetFields()

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
            if line - n >= 0 and 0 <= y < self.size:
                p = self.coord2pos(line - n, y)
                l.append(p)

            if line + n < self.size and 0 <= y < self.size:
                p = self.coord2pos(line + n, y)
                l.append(p)

        for x in range(int(line - n + 1), int(line + n)):
            if col - n >= 0 and 0 <= x < self.size:
                p = self.coord2pos(x, col - n)
                l.append(p)

            if col + n < self.size and 0 <= x < self.size:
                p = self.coord2pos(x, col + n)
                l.append(p)

        return set(l)

    def resetFields(self):
        for case in self.grid:
            case.fields = {}

    def birthControl(self):
        if Veine.count >= Veine.max: return
        best = None
        bestPos = None
        for agent in self.agents:
            if type(agent) == Veine:
                neighbor = self.neighbor(*agent.coord, 1)
                for n in neighbor:
                    if self.grid[n].agent is None:
                        if best is None:
                            best = self.grid[n]
                            bestPos = n
                        elif 'food' in self.grid[n].fields and 'food' not in best.fields:
                            best = self.grid[n]
                            bestPos = n
                        elif 'food' in self.grid[n].fields and 'food' in best.fields:
                            if self.grid[n].fields['food'] > best.fields['food']:
                                best = self.grid[n]
                                bestPos = n
                        elif 'food' not in self.grid[n].fields and 'food' in best.fields:
                            continue
                        elif randint(0, 10) > 5:
                            best = self.grid[n]
                            bestPos = n

        if best != None:
            newVeine = Veine(*self.pos2coord(bestPos))
            best.agent = newVeine
            self.agents.append(newVeine)

    def sarahConnor(self):
        if Veine.count < Veine.max: return

        worst = None
        for agent in self.agents:
            if type(agent) == Veine:
                pos = self.coord2pos(*agent.coord)

                if worst is None:
                    worst = self.grid[pos]
                elif 'food' not in self.grid[pos].fields and 'food' in worst.fields:
                    worst = self.grid[pos]
                elif 'food' not in self.grid[pos].fields and 'food' not in worst.fields:
                    if randint(0, 10) > 5:
                        worst = self.grid[pos]
                elif 'food' in self.grid[pos].fields and 'food' in worst.fields:
                    if self.grid[pos].fields['food'] < worst.fields['food']:
                        worst = self.grid[pos]

        if worst is not None:
            Veine.count -= 1
            self.agents.remove(worst.agent)
            worst.agent = None

    def tick(self):
        self.setField()
        self.sarahConnor()
        self.birthControl()

    def run(self, loop):
        for i in range(loop):
            self.tick()
