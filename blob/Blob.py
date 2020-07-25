#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-14"

from random import randint, choice

from blob import Food
from blob.Spore import Spore
from blob.Vein import Vein


class Blob(object):
    """The Blob represent a physarum polycephalum simulated in the world
        :param Case case1: starting position of the blob
        :param Case case2: position of the second vein
        :param int id:
        :paarm World world:
        """

    def __init__(self, world, id_blob, case1, case2, sex = None):
        self._id = id_blob
        self._world = world
        self._learning = 1
        self._hungry = False
        if sex is None:
            self._sex = randint(0, 720)
        else: self._sex = sex
        self._veins = []
        self._cases = []
        self._max = 5
        self._age = 1

        self._moisture = 0.6
        self._glucides = 5  # nb_veines
        self._proteines = 5 # masse
        self._nutrition_state = 100

        self._sclerote = False
        self._dead = False

        v1 = self._createVein(case1, None)
        v2 = self._createVein(case2, v1)

    @property
    def isSclerote(self):
        return self._sclerote

    @property
    def Id(self):
        return self._id

    @property
    def isDead(self):
        return self._dead

    @property
    def Age(self):
        return self._age

    def StuckInMucus(self):
        """
        Return true if the physarum is surrounded by mucus
        """
        for vein in self._veins:
            for n in vein.Case.Neighborhood:
                if n not in self._cases:
                    if not n.Mucus:
                        return False

        return True

    def Moisturize(self, moisture):
        """
        Manages physarum humidity
        :param double moisture: humidity of the world
        """
        factor = 0.01
        self._moisture = min(max(0, self._moisture + (moisture * factor)), 1)

    def Dessication(self):
        """
        Set the sclerote transformation
        """
        self._nutrition_state = 100
        self._sclerote = True

    def Rehydrate(self):
        """
        Reset the physarum after dessication
        """
        self._sclerote = False

    def Sporulation(self):
        """
        Turn the physarum into spores
        """
        list = []
        for c in self._cases:
            c.RemoveVein()
            s = Spore(self._sex, c)
            c.AddSpore(s)
            list.append(s)

        self._veins = []
        self._cases = []
        self._dead = True

        return list

    def FoodState(self):
        """
        Return the state of the blob according its nutrition state
        :return: string
        """
        if self._nutrition_state <= 0:
            return "faim"
        elif self._proteines / self._glucides > 7:
            return "split"
        elif self._glucides / self._proteines > 7:
            return "mort"
        else:
            return "vit"

    def MoistureState(self):
        """
        Return the state of the blob according its moisture state
        :return: int
        """
        if self._moisture < 0.5:
            return -1
        if 0.5 <= self._moisture <= 0.8:
            return 0
        else:
            return 1

    def JustALittleOlder(self):
        """
        Performs aging on the blob
        """
        self._age += 1

    def Starve(self):
        """
        Physarum polycephalum uses its nutrients over time
        """
        self._nutrition_state -= 1
        self._learning = max(1, self._learning - 0.1)

    def Feed(self):
        food = None

        if self._hungry <= 40:
            for c in self._cases:
                if c.isIn([Food]) and c.Vein is not None:
                    for a in c.Agents:
                        if type(a) == Food: food = a

                    qte = food.Eat()
                    self._proteines += qte['proteine']
                    self._glucides += qte['glucide']

                    self._max = int(self._proteines)
                    self._nutrition_state += 10

                    if not food.State:
                        return food, c.Position

        return False

    def _killVein(self):
        """
        Remove the least interesting vein for physarum polycephalum
        """
        worst = self._findWorst()
        if worst is None:
            return

        self._cases.remove(worst)
        self._veins.remove(worst.Vein)
        worst.Vein.Kill()
        worst.RemoveVein()
        worst.AddMucus()

    def _addVein(self, neighborhood=False):
        """
        Add a vein in an interesting position for physarum polycephalum if the maximum number of veins is not reached
        :param bool neighborhood: if true, search for the best position among the boxes next to the veins,
            if not, search add a vein on an available box around the best vein (default: False)
        """
        if len(self._veins) < self._max:
            if neighborhood:
                case, parent = self._findBestNeighbor()
                self._createVein(case, parent)
            else:
                vein = self._findBestVein()
                if self._letsMakeLive(vein) == 'merged': return 'merged'

    def MoveAndGrow(self):
        """
        Manages physarum movement
        """
        self._killVein()
        if self._addVein() != 'merged':
            self._addVein()

    def Learn(self):
        """
        Manages physarum learning
        :param double moisture: humidity of the world
        """
        for c in self._cases:
            if c.Salt:
                self._learning += 0.2

    def Die(self):
        """
        Manages physarum death
        """
        self._dead = True

    def IncrementMax(self, qte=1):
        """
        Add a quantity for the maximum number of veins
        """
        self._max += qte

    def Merge(self, blob):
        """
        Manages merging between two physarum
        """
        self._world.RemoveBlob(blob)
        self.IncrementMax(blob._max)

        for v in blob._veins:
            v._blob = self
            self._veins.append(v)

        for c in blob._cases:
            self._cases.append(c)

    def _findBestNeighbor(self):
        pass

    def _availableWithMucus(self, case):
        neighbors = case.Neighborhood
        for c in neighbors:
            if c.Vein is None:
                return True

        return False

    def _hasAvailableNeighbors(self, case):
        neighbors = case.Neighborhood
        for c in neighbors:
            if c.Vein is None and not c.Mucus:
                return True

        return False

    def _findBestVein(self):
        best = []
        maxDetected = -10

        availables = []
        lastChoice = []

        for c in self._cases:
            if self._availableWithMucus(c):
                lastChoice.append(c)
            if self._hasAvailableNeighbors(c):
                availables.append(c)
                for e in self._world._emitters:
                    distance = self._tchebychevDistance(c.Position, e.Position)
                    if distance <= e.Distance:
                        powerDetected = e.Power + (e.Decay * distance)
                        # powerDetected = e.power + (e.decay * distance) + c._value
                        # powerDetected = c._value
                        if powerDetected > maxDetected:
                            maxDetected = powerDetected
                            best = [c]
                        elif powerDetected == maxDetected:
                            best.append(c)

        if len(best) == 0:
            if len(availables) == 0:
                return choice(lastChoice)
            else:
                return choice(availables)
        if len(best) == 1:
            return best[0]
        if len(best) == len(self._veins):
            return best[-1]
        return choice(best)

    def _findWorst(self):
        worst = []
        for c in self._cases:
            neighbors = self._world._neighborhood(c, self._world._time_in_mucus[self._id])
            v = 0

            for pos in neighbors:
                case = pos
                if not case.Mucus: v += 1

            c.MergeField(v)

            if c.Vein.isExtremity and not c.isIn([Food]):
                if len(worst) == 0:
                    worst.append(c)
                elif c.Field < worst[0].Field:
                    worst = [c]
                elif c.Field == worst[0].Field:
                    worst.append(c)

        if len(worst) == 0:
            return None
        w = choice(worst)
        return w

    def _createVein(self, case, parent=None):
        if case.Vein is not None and case.Vein.Blob != self and parent is not None:
            case.Vein.Parent = parent
            parent._children.append(self)
            case.Vein.Blob.Merge(self)
            return "merged"
        else:
            v = Vein(self, case, parent)
            self._veins.append(v)
            self._cases.append(case)

            case.AddVein(v)
            return v

    def _letsMakeLive(self, case):
        neighbors = case.Neighborhood
        available = []
        withMucus = []
        for c in neighbors:
            if (c.Vein is None or c.Vein.Blob != self) and not c.Mucus:
                available.append(c)
            if c.Vein is None or c.Vein.Blob != self:
                withMucus.append(c)

        if len(available) == 0:
            nb = randint(0, len(withMucus))
            if self._createVein(choice(withMucus), case.Vein) == 'merged': return 'merged'
        else:
            nb = randint(0, len(available))
            if self._createVein(choice(available), case.Vein) == 'merged': return 'merged'

    def _tchebychevDistance(self, posA, posB):
        (xA, yA) = self._world._pos2coord(posA)
        (xB, yB) = self._world._pos2coord(posB)

        return max(abs(xA - xB), abs(yA - yB))
