#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-14"

from random import random, choice

from blob import Case, Blob, Food, Emitter


class World(object):
    """The World object is an object that manages the simulation
        :param int nb_cases: number of line and columns to use for the simulation
        :param int pos: start position of the physarum
        :param int total_size: size of the simulated world (in centimeters)
        """

    count_blob = 0

    def __init__(self, nb_cases, total_size, tick=1):
        self._spores = []
        self._line = nb_cases
        self._col = nb_cases
        self._grid = [Case(i, (i // nb_cases, i % nb_cases)) for i in range(nb_cases ** 2)]
        for c in self._grid:
            c.SetNeighborhood(self._neighborhood(c))

        self._total_size = total_size

        # simulation elements
        self._time_tick = tick
        self._elapsed_time = 0
        self._temperature = 27
        self._moisture = 0

        self._emitters = []

        self._blobs = []
        self._time_in_mucus = {}

    @property
    def TimeTick(self):
        return self._time_tick

    @property
    def ElapsedTime(self):
        return self._elapsed_time

    @property
    def Grid(self):
        return self._grid

    @property
    def Size(self):
        return self._line

    def SetMoisture(self, value):
        if 0 <= value <= 46:
            self._moisture = -1
        elif 47 <= value <= 80:
            self._moisture = 0
        else:
            self._moisture = 1

    def SetTemperature(self, value):
        self._temperature = value

    def _neighborhood(self, case, n=1):
        """
        Look for the neighbors at a given distance (Moore neighborhood)
        :param Case case: box whose neighbors we must look for
        :param n: The distance to look for neighbors
        :return: a list of boxes corresponding to the neighbors
        """
        line, col = case.Coord

        n_list = []
        for y in range(int(col - n), int(col + n + 1)):
            if line - n >= 0 and 0 <= y < self._col:
                p = self.Coord2pos(line - n, y)
                n_list.append(self._grid[p])

            if line + n < self._line and 0 <= y < self._col:
                p = self.Coord2pos(line + n, y)
                n_list.append(self._grid[p])

        for x in range(int(line - n + 1), int(line + n)):
            if col - n >= 0 and 0 <= x < self._line:
                p = self.Coord2pos(x, col - n)
                n_list.append(self._grid[p])

            if col + n < self._col and 0 <= x < self._line:
                p = self.Coord2pos(x, col + n)
                n_list.append(self._grid[p])

        return set(n_list)

    def _neighborhoodPos(self, pos, n=1):
        """
        Look for the neighbors at a given distance (Moore neighborhood)
        :param int pos: pos whose neighbors we must look for
        :param n: The distance to look for neighbors
        :return: a list of positions corresponding to the neighbors
        """
        line, col = self._pos2coord(pos)

        n_list = []
        for y in range(int(col - n), int(col + n + 1)):
            if line - n >= 0 and 0 <= y < self._col:
                n_list.append(self.Coord2pos(line - n, y))

            if line + n < self._line and 0 <= y < self._col:
                n_list.append(self.Coord2pos(line + n, y))

        for x in range(int(line - n + 1), int(line + n)):
            if col - n >= 0 and 0 <= x < self._line:
                n_list.append(self.Coord2pos(x, col - n))

            if col + n < self._col and 0 <= x < self._line:
                n_list.append(self.Coord2pos(x, col + n))

        return set(n_list)

    def _pos2coord(self, pos):
        """
        Convert position to coordinates
        :param pos: A position in the world
        :return: (line, col) corresponding to the given position
        """
        line = pos // self._col
        col = pos % self._col
        return line, col

    def Coord2pos(self, line, col):
        """
        Convert coordinate to position
        :param line:
        :param col:
        :return: the position corresponding to the given coordinates
        """
        return int(line * self._col + col)

    def AddEmitter(self, agent, pos):
        """
        Adds an agent emitting an attracting or repelling field in the world
        :param Agent agent: agent to add in the world
        :param int pos: position of the agent
        """
        self._grid[pos].AddAgent(agent)
        self._emitters.append(agent)

    def RemoveAgent(self, agent, pos):
        """
        Delete an agent from the world
        :param Agent agent: agent to remove in the world
        :param int pos: position of the agent
        """
        self._emitters.remove(agent)
        self._grid[pos].RemoveAgent(agent)

    def _computeField(self):
        """
        Compute the field emitted by each agent on the grid
        """
        self._resetFields()

        for e in self._emitters:
            d = e.Decay

            for i in range(abs(d)):
                neighbors = self._neighborhood(self._grid[e.Position], i)

                for n in neighbors:
                    # special treatment so that the mucus fields do not merge
                    if e.Name == "mucus":
                        n.SetField = (e.Power + ((e.Power / e.Decay) * i))
                    else:
                        n.MergeField(e.Power + ((e.Power / e.Decay) * i))

    def _resetFields(self):
        """
        resets the fields in each box
        """
        for case in self._grid:
            case.ResetField()

    def _updateBlobState(self, blob):
        """
        Update blob state according world's elements
        :param Blob blob: the blob to update
        """
        if self._temperature < 5:  # mort
            blob.Die()
            # self._blobs.remove(blob)
        elif self._temperature >= 40:  # mort
            blob.Die()
            # self._blobs.remove(blob)
        else:
            if blob.MoistureState() == -1:
                if blob.FoodState() == "faim":
                    blob.Dessication()
                elif blob.FoodState() == "split":
                    pass  # split
                elif blob.FoodState() == "mort":  # mort
                    blob.Die()
                    # self._blobs.remove(blob)
                else:
                    pass  # vit
            elif blob.MoistureState() == 1:
                if blob.FoodState() == "faim":
                    self._spores.extend(blob.Sporulation())
                    self._blobs.remove(blob)
                elif blob.FoodState() == "split":
                    pass  # split
                elif blob.FoodState() == "mort":
                    blob.Die()
                    # self._blobs.remove(blob)
                else:
                    blob.Rehydrate()
            else:
                if blob.FoodState() == "faim":
                    blob.Die()
                elif blob.FoodState() == "split":
                    pass  # split
                elif blob.FoodState() == "mort":

                    blob.Die()
                    # self._blobs.remove(blob)
                else:
                    blob.Rehydrate()

    def Tick(self):
        """
        Performs a simulation lap according to the selected time and the simulation size
        """
        nb_tick = int((self._line * self._time_tick) / self._total_size)
        self._elapsed_time += self._time_tick

        for _ in range(nb_tick):
            self._computeField()

            for blob in self._blobs:
                # if there are case without mucus, this will enlarge the research to get out of the mucus
                if blob.StuckInMucus():
                    self._time_in_mucus[blob.Id] += 1
                else:
                    self._time_in_mucus[blob.Id] = 1

                # at each turn, the blob is affected by the ambient humidity
                if self._moisture > blob.MoistureState(): direction = 1
                elif self._moisture < blob.MoistureState(): direction = -1
                else: direction = 0

                blob.Moisturize(direction)

                blob.JustALittleOlder()

                # the blob moves and feeds less quickly as it ages, this is randomly simulated following an age factor
                t = random()
                age_factor = 720

                if not blob.isSclerote and not blob.isDead and t < age_factor / blob.Age:
                    blob.Starve()

                    food_state = blob.Feed()
                    if food_state:
                        self.RemoveAgent(food_state[0], food_state[1])

                    blob.Learn()

                    blob.MoveAndGrow()

                self._updateBlobState(blob)

            for spore in self._spores:
                if spore.Move(spore.Case.Neighborhood):
                    self._spores.remove(spore)
                    self.AddBlob(spore.Case.Position, spore.Sex)

    def AddFood(self, qte, concentration, ratio, pos):
        """
        Add food in the world
        :param int qte: Food quantity
        :param double concentration: Food concentration
        :param double ratio: Food ratio
        :param int pos: Position where to add food
        """
        food = Food(pos, -100, qte, concentration, ratio)
        self.AddEmitter(food, pos)

    def AddSalt(self, pos):
        """
        Add salt in the world
        :param int pos: Position where to add salt
        """
        self._grid[pos].AddSalt()

    def AddLight(self, pos):
        """
        Add a pointlight in the world
        :param int pos: Position where to add the light
        """
        light = Emitter('Light', pos, 10, -1)
        self.AddEmitter(light, pos)

    def AddBlob(self, pos, sex=None):
        """
        Add a physarum at the given position
        :param int pos: Position where to add the blob
        """
        World.count_blob += 1
        self._time_in_mucus[World.count_blob] = 0
        neighbors = self._neighborhood(self._grid[pos])
        pos2 = choice(list(neighbors))

        if self._grid[pos].Vein is None and pos2.Vein is None:
            self._blobs.append(Blob(self, World.count_blob, self._grid[pos], pos2, sex))

    def RemoveBlob(self, blob):
        self._blobs.remove(blob)