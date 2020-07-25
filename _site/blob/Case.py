#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-14"


class Case(object):
    """The Case object is an object allowing manipulations in the world
        :param int pos: position of the case in the grid's world
        :param tuple coord: coordinates of the case in the grid's world
        """

    def __init__(self, pos, coord):
        self._position = pos
        self._coord = coord
        self._field_value = 0
        self._agents = []
        self._spores = []
        self._neighbors = []
        self._vein = None
        self._mucus = False
        self._update = False
        self._salt = False

    @property
    def Updated(self):
        return self._update

    @property
    def Mucus(self):
        return self._mucus

    @property
    def Neighborhood(self):
        return self._neighbors

    @property
    def Spores(self):
        return self._spores

    @property
    def Salt(self):
        return self._salt

    @property
    def Agents(self):
        return self._agents

    @property
    def Position(self):
        return self._position

    @property
    def Vein(self):
        return self._vein

    @property
    def Coord(self):
        return self._coord

    @property
    def Field(self):
        return self._field_value

    def ResetField(self):
        """
        Reset the field in that box
        """
        self._field_value = 0

    def isIn(self, typeList):
        for t in typeList:
            unType = False
            for a in self._agents:
                if type(a) == t: unType = True

            if not unType: return False

        return True

    def FinishUpdate(self):
        self._update = False

    def AddSalt(self):
        self._update = True
        self._salt = True

    def AddAgent(self, agent):
        """
        Add an agent in the box
        :param Agent agent: agent to add
        """
        self._update = True
        self._agents.append(agent)

    def RemoveAgent(self, agent):
        """
        Remove an agent from the box
        :param Agent agent: agent to remove
        """
        self._update = True
        self._agents.remove(agent)

    def AddVein(self, vein):
        self._update = True
        self._vein = vein

    def AddMucus(self):
        self._mucus = True

    def RemoveVein(self):
        self._update = True
        self._vein = None

    def AddSpore(self, spore):
        self._update = True
        self.Spores.append(spore)

    def RemoveSpore(self, spore):
        self._update = True
        self.Spores.remove(spore)

    def MergeField(self, value):
        self._field_value += value

    def SetField(self, value):
        self._field_value = value

    def SetNeighborhood(self, neighborhood):
        self._neighbors = neighborhood

    def TimeToken(self):
        spores = []
        if len(self._spores) > 1 and self._vein is None:
            sex = self._spores[0].Sex
            spores.append(self._spores[0])
            for i in range(1, len(self._spores)):
                if sex != self._spores[i].Sex:
                    spores.append(self._spores[i])
                    return spores

        return []
