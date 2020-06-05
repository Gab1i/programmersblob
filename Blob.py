from Food import Food
from Veine import Veine
from random import choice, random


class Blob:
    def __init__(self, world, pos):
        self.world = world

        self._max = 50
        self._veines = []
        self._cases = []
        self._neighborhood = []

        self._createVeine(self.world.grid[pos])
        self._createVeine(self.world.grid[max(pos - 1, 0)])

        # Modes :
        #  - exploration : Pas de cible, s'étend
        #  - target : Cible acquired, se meut
        self._behavior = 'Exploration'

    def _createVeine(self, case):
        v = Veine()

        self._veines.append(v)
        self._cases.append(case)
        case.agents.append(v)

        self._getNeighborhood()

    def _destroyVeine(self, case):
        v = None
        for a in case.agents:
            if type(a) == Veine: v = a

        self._veines.remove(v)
        case.agents.remove(v)
        self._cases.remove(case)

        self._getNeighborhood()

    def _getNeighborhood(self):
        self._neighborhood = []

        for c in self._cases:
            neighbors = self.world.Neighborhood(c)
            for n in neighbors:

                add = True

                for a in n.agents:
                    if type(a) == Veine: add = False

                if add:
                    self._neighborhood.append(n)

    def _findBest(self):
        best = []

        if all(n.mucus for n in self._neighborhood):
            return choice(self._neighborhood)

        for c in self._neighborhood:
            if c.mucus == False:
                if len(best) == 0:
                    best.append(c)
                elif c.getField() > best[0].getField():
                    best = [c]
                elif c.getField() == best[0].getField():
                    best.append(c)

        return choice(best)

    def _findWorst(self):
        worst = []
        for c in self._cases:
            if len(worst) == 0:
                worst.append(c)
            elif c.getField() < worst[0].getField():
                worst = [c]
            elif c.getField() == worst[0].getField():
                worst.append(c)

        w = choice(worst)
        return w

    def Kill(self):
        if self._behavior == 'Target':
            prob = 0.9
        elif self._behavior == 'Exploration':
            prob = 0.5

        if random() <= prob:
            w = self._findWorst()
            w.mucus = True
            self._destroyVeine(w)

    def Add(self):
        if len(self._veines) < self._max:
            self._createVeine(self._findBest())

    def Feed(self):
        veine = None
        food = None

        for c in self._cases:
            print(c)
            if c.isIn([Food, Veine]):
                for a in c.agents:
                    if type(a) == Food: food = a

                self._max += 1
                food.Eat(1)
                if not food.status: self.world.DeleteAgent(food, c.position)

    @property
    def neighborhood(self):
        return self._neighborhood
