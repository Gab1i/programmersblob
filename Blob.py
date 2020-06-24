from Emetteur import Emetteur
from Food import Food
from Node import Node
from Veine import Veine
from random import choice, random, randint


class Blob:
    def __init__(self, world, pos):
        self.world = world

        self._max = 5
        self._veines = []
        self._cases = []
        self._neighborhood = []

        # self._proteines = 0
        # self._glucides = 0

        self._nbVeines = 5 # glucide
        self._masse = 5 # proteines

        # nbVeine -- + masse -- => sclerote ou sporulation (question : la difference sur l'environnement)
        # mode exploration : (moins de nutriment=proteines+glucides) ca s'étend, plus de veines
        # mode exploitation :

        self._substancesDiversesEtVariees = {}

        v = self._createVeine(None, self.world.grid[pos])
        self._createVeine(v, self.world.grid[max(pos - 1, 0)])

        # Modes :
        #  - exploration : Pas de cible, s'étend
        #  - target : Cible acquired, se meut

        # Naissance entre 1 et nb de voisins sur le best
        # Mort mucus
        # Champs de 1 avec mucus
        # Session interface/Design/Couleur/Menu/Ecrand'accueil/PannO2Kontrol
        # Champ d'agitation - Tester

        self._behavior = 'Exploration'

    def _deathRatio(self):
        # ratio de mort > XX tu meurs
        return self._nbVeines / self._masse

    def _splitRatio(self):
        # ratio de split > XX # tu split
        return self._masse / self._nbVeines

    def _createVeine(self, veineParent, case):
        v = Veine(veineParent)
        # ("je suis {0}, engendré par {1}".format(case[1], case[0]))

        self._veines.append(v)
        self._cases.append(case)
        case.Veine = v

        self._getMixedNeighborhood()
        # self._getNeighborhood()

    def _destroyVeine(self, case):

        v = case.Veine

        """if case.parent is not None:
            case.parent.child = max(0, case.parent.child-1)
        else:
            for child in case.children:
                child.parent = None"""
        v.Kill()

        self._veines.remove(v)
        case.Veine = None
        self._cases.remove(case)

        self._getMixedNeighborhood()
        # self._getNeighborhood()

    @property
    def neighborhood(self):
        return self._neighborhood

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

    def _getMixedNeighborhood(self):
        self._neighborhood = []

        for c in self._cases:
            neighbors = self.world.Neighborhood(c)
            for n in neighbors:
                if n.Veine is None: self._neighborhood.append((c.Veine, n))

    def Grow(self):
        for v in self._veines:
            v.Grow()

    def _findBest(self):
        # Code qui marche
        best = []

        if all(n[1].mucus for n in self._neighborhood):
            return choice(self._neighborhood)

        for c in self._neighborhood:
            if not c[1].mucus:
                if len(best) == 0:
                    best.append(c)
                elif c[1].getField() > best[0][1].getField():
                    best = [c]
                elif c[1].getField() == best[0][1].getField():
                    best.append(c)

        theChoice = choice(best)
        return theChoice[0], theChoice[1]

    def _findBest(self):
        # Code qui marche
        best = []

        if all(n[1].mucus for n in self._neighborhood):
            return choice(self._neighborhood)

        for c in self._neighborhood:
            if not c[1].mucus:
                if len(best) == 0:
                    best.append(c)
                elif c[1].getField() > best[0][1].getField():
                    best = [c]
                elif c[1].getField() == best[0][1].getField():
                    best.append(c)

        theChoice = choice(best)
        return theChoice[0], theChoice[1]

    def _findTheBestLiving(self):
        # Cherche le meilleur en fonction de la distance au mangeage
        best = []
        maxDetected = -10

        availables = []

        for c in self._cases:
            if self._hasAvailableNeighbors(c):
                availables.append(c)
                for e in self.world._emitters:
                    distance = self._tchebychevDistance(c.position, e.pos)
                    if distance <= e.distance:
                        powerDetected = e.power + (e.decay * distance)
                        if powerDetected > maxDetected:
                            maxDetected = powerDetected
                            best = [c]
                        elif powerDetected == maxDetected:
                            best.append(c)

        if len(best) == 0:
            return choice(availables)
        if len(best) == 1:
            return best[0]

        return choice(best)

    def _findTheBestLiving(self):
        # Cherche le meilleur en fonction du contenu du mangeage
        # revoir ça à un moment
        best = []
        maxDetected = -10

        availables = []

        for c in self._cases:
            if self._hasAvailableNeighbors(c):
                availables.append(c)

                for e in self.world._emitters:
                    distance = self._tchebychevDistance(c.position, e.pos)
                    if distance <= e.distance:
                        powerDetected = e.power + ((e.power/e.decay) * distance)
                        if powerDetected > maxDetected:
                            maxDetected = powerDetected
                            best = [c]
                        elif powerDetected == maxDetected:
                            best.append(c)

        if len(best) == 0:
            return choice(availables)
        if len(best) == 1:
            return best[0]

        return choice(best)

    def _hasAvailableNeighbors(self, case):
        neighbors = self.world.Neighborhood(case)
        for c in neighbors:
            if c.Veine is None and not c.mucus: return True

        return False

    def _letsMakeLive(self, case):
        neighbors = self.world.Neighborhood(case)
        available = []
        for c in neighbors:
            if c.Veine is None and not c.mucus: available.append(c)

        nb = randint(0, len(available))
        #for i in range(1):
        #   self._createVeine(case.Veine, available.pop())
        self._createVeine(case.Veine, choice(available))

    def _tchebychevDistance(self, posA, posB):
        (xA, yA) = self.world.pos2coord(posA)
        (xB, yB) = self.world.pos2coord(posB)

        return max(abs(xA - xB), abs(yA - yB))

    def _findWorst(self):
        worst = []
        for c in self._cases:
            if c.Veine.isExtremity and not c.isIn([Food]):
                if len(worst) == 0:
                    worst.append(c)
                elif c.getField() < worst[0].getField():
                    worst = [c]
                elif c.getField() == worst[0].getField():
                    worst.append(c)
        if len(worst) == 0: return None
        w = choice(worst)
        return w

    def Kill(self):
        """if self._behavior == 'Target':
            prob = 0.9
        elif self._behavior == 'Exploration':
            prob = 0.1"""
        prob = 1

        if random() <= prob:
            w = self._findWorst()
            if w is None: return
            # w.Veine.Shrink()
            # if w.Veine._size < 1:
            # w.mucus = True
            # self.world.AddEmitter(Emetteur('Le Mucus', w.position, -2, 1), w.position)
            # self._destroyVeine(w)

            w.mucus = True
            self.world.AddEmitter(Emetteur('Le Mucus', w.position, -2, 1), w.position)
            self._destroyVeine(w)

    def Add(self):
        # if len(self._veines) < self._max:
        #   self._createVeine(*self._findBest())
        if len(self._veines) < self._max:
            case = self._findTheBestLiving()
            self._letsMakeLive(case)

    def Feed(self):
        veine = None
        food = None

        for c in self._cases:
            if c.isIn([Food]) and c.Veine is not None:
                for a in c.agents:
                    if type(a) == Food: food = a

                qte = food.Eat()
                self._masse += qte['proteine']
                self._nbVeines += qte['glucide']

                if not food.status: self.world.DeleteAgent(food, c.position)
