# -*- coding: utf-8 -*-
from Agent import *
from Case import Case
from random import randint


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
        return line, col

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
        Compute the field emitted by each agent on the grid
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

    def vonNeumannNeighborhood(self, line, col):
        l = []

        if line >= 0:
            l.append(self.coord2pos(line - 1, col))

        if line < self.size - 1:
            l.append(self.coord2pos(line + 1, col))

        if col >= 0:
            l.append(self.coord2pos(line, col - 1))

        if col < self.size - 1:
            l.append(self.coord2pos(line, col + 1))

        return l

    def angularNeighborhood(self, line, col):
        l = []

        if line >= 0:
            if col >= 0: l.append(self.coord2pos(line - 1, col - 1))
            if col < self.size - 1: l.append(self.coord2pos(line - 1, col + 1))

        if col >= 0 and line < self.size - 1:
             l.append(self.coord2pos(line + 1, col - 1))

        if col < self.size - 1 and line < self.size - 1:
            l.append(self.coord2pos(line + 1, col + 1))

        return l

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

        self.action()

        #self.sarahConnor()
        #self.birthControl()

    def getBest(self):
        best = None
        bestPos = None

        for agent in self.agents:
            if type(agent) == Veine:
                pos = self.coord2pos(*agent.coord)

                neighbor = self.neighbor(*agent.coord, 1)
                for n in neighbor:
                    if type(self.grid[n].agent) != Food and self.grid[n].agent is None:
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
                        elif randint(0, 10) > 8:
                            best = self.grid[n]
                            bestPos = n

        return best, bestPos

    def getWorst(self):
        worst = None
        for agent in self.agents:
            if type(agent) == Veine:
                howManyVeines = 0
                for n in self.vonNeumannNeighborhood(*agent.coord):
                    if type(self.grid[n].agent) == Veine: howManyVeines += 1
                if howManyVeines > 1: continue

                howManyVeines = 0
                for n in self.angularNeighborhood(*agent.coord):
                    if type(self.grid[n].agent) == Veine: howManyVeines += 1
                if howManyVeines > 1: continue

                pos = self.coord2pos(*agent.coord)

                neighbor = self.neighbor(*agent.coord, 1)
                for n in neighbor:
                    if type(self.grid[n].agent) != Food and self.grid[n].agent is None:
                        if worst is None:
                            worst = self.grid[pos]
                        elif 'food' not in self.grid[pos].fields and 'food' in worst.fields:
                            worst = self.grid[pos]
                        elif 'food' not in self.grid[pos].fields and 'food' not in worst.fields:
                            if randint(0, 10) > 8:
                                worst = self.grid[pos]
                        elif 'food' in self.grid[pos].fields and 'food' in worst.fields:
                            if self.grid[pos].fields['food'] < worst.fields['food']:
                                worst = self.grid[pos]

        return worst

    def lookForFood(self, line, col):
        print(self.neighbor(line, col, 1))
        for n in self.neighbor(line, col, 1):
            print(self.grid[n].agent)
            if type(self.grid[n].agent) == Food:
                return self.grid[n].agent

        return False

    def action(self):

        worst = self.getWorst()
        self.kill(worst)

        best, bestPos = self.getBest()

        for agent in self.agents:
            print(agent)
            if type(agent) == Veine:
                f = self.lookForFood(*agent.coord)
                print('je cherche')
                if f != False:
                    agent.feed(f)
                    print('J\'ai à manger !! Youpi')

            if type(agent) == Food:
                print("Je suis en {0}".format(self.coord2pos(*agent.coord)))
                if agent.qte == 0:
                    self.agents.remove(agent)
                    pos = self.coord2pos(*agent.coord)
                    self.grid[pos].agent = None


        self.birth(best, bestPos)

    def run(self, loop):
        for i in range(loop):
            self.tick()

    def kill(self, worst):
        if Veine.count < Veine.max: return

        if worst is not None:
            Veine.count -= 1
            self.agents.remove(worst.agent)
            worst.agent = None

    def birth(self, best, bestPos):
        if best != None:
            newVeine = Veine(*self.pos2coord(bestPos))
            best.agent = newVeine
            self.agents.append(newVeine)

