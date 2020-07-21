from random import random

from Blob import Blob
from Case import *

class World:
    def __init__(self, line, col, pos):
        self.line = line
        self.col = col
        self.grid = [Case(i, (line, col)) for i in range(line * col)]


        self._blobs = [Blob(self, pos)]
        self._blobs.append(Blob(self, 24))
        self._emitters = []

        self._spores = []

        self._light = 1

        # -1 : monde sec
        # 0 : monde normal
        # 1 : monde très humide
        self._moisture = 1

        self._temperature = 27

        self._timeInTheMucus = 1

        self.nombreHeureParTick = 1
        self.ellapsedTime = 0
        self.tailleTotale = 10


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
        age_factor = 720
        nbTick = round((self.line * self.nombreHeureParTick) / self.tailleTotale)
        self.ellapsedTime += self.nombreHeureParTick

        s = 0
        for _ in range(nbTick):

            self.ComputeField()
            for blob in self._blobs:
                if blob.ToutDansLeMucus(): self._timeInTheMucus += 1
                else: self._timeInTheMucus = 1

                blob.Moisturize(self._moisture)
                t = random()
                blob._age += 1

                if not blob._sclerote and not blob._dead and t < age_factor/blob._age:
                    blob._etatNutritif -= 1
                    blob.apprentissage = max(1, blob.apprentissage - 0.1)

                    blob.Feed()

                    blob.Learn()

                    blob.Kill()

                    blob.Add()
                    blob.Add()

                self.CheckBlobState(blob)

            for spore in self._spores:
                if spore.Move(self.Neighborhood(spore._case, 1)):
                    self._spores.remove(spore)
                    self._spores.remove()
                    self.newBlob(spore._case.position, spore._sexe)


    def RemoveBlob(self, blob):
        self._blobs.remove(blob)
        print("J'ai fussssssssionné")


    def newBlob(self, pos, sexe):
        print("Un nouveau blob")
        self._blobs.append(Blob(self, pos, sexe))

    def CheckBlobState(self, blob):
        if self._temperature < 5: # mort
            blob.Die()
            #self._blobs.remove(blob)
        elif self._temperature >= 40: # mort
            blob.Die()
            #self._blobs.remove(blob)
        else:
            if blob.GetMoistureState() == -1:
                if blob.GetFoodStatus() == "faim":
                    blob.Dessication()
                elif blob.GetFoodStatus() == "split":
                    pass # split
                elif blob.GetFoodStatus() == "mort": # mort
                    blob.Die()
                    #self._blobs.remove(blob)
                else:
                    pass # vit
            elif blob.GetMoistureState() == 1:
                if blob.GetFoodStatus() == "faim":
                    self._spores.extend(blob.Sporulation())
                    self._blobs.remove(blob)
                elif blob.GetFoodStatus() == "split":
                    pass  # split
                elif blob.GetFoodStatus() == "mort":
                    blob.Die()
                    #self._blobs.remove(blob)
                else:
                    blob.Rehydrate()
            else:
                if blob.GetFoodStatus() == "faim":
                    blob.Die()
                elif blob.GetFoodStatus() == "split":
                    pass  # split
                elif blob.GetFoodStatus() == "mort":

                    blob.Die()
                    #self._blobs.remove(blob)
                else:
                    blob.Rehydrate()


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
                    if e.name == "Le Mucus": n._value = (e.power + ((e.power/e.decay) * i))
                    else: n.setField(e.power + ((e.power/e.decay) * i))



    def resetFields(self):
        for c in self.grid:
            c.resetField()
