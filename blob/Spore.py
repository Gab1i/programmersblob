#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-14"

from random import randint


class Spore(object):
    """A spore is a cell used in the sexual reproduction of physarum polycephalum
        :param int sex: sex of the spore (720 possibilities)
        :param Case case: position of the spore
        """
    def __init__(self, sex, case):
        self._sex = sex
        self._case = case

    @property
    def Case(self):
        return self._case

    @property
    def Sex(self):
        return self._sex

    def Move(self, neighbors):
        """
        Performs the movement of the spore
        """
        neighbors = list(neighbors)
        r = randint(0, len(neighbors)-1)

        case = neighbors[r]
        case.AddSpore(self)
        self._case.RemoveSpore(self)
        self._case = case

        if len(self._case.TimeToken()) == 2:
            #self._case.Spores = []
            return True

        return False
