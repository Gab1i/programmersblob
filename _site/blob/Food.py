#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-23"

from blob import Emitter


class Food(Emitter):
    """Food is used to food the physarum
        :param int name: starting position of the blob
        :param int pos: position of the food in the world
        :param int decay:
        :param int qte: quantity of food before it diseappear
        :param double concentration: concentration of food between 0 and 1
        :param double ratio: ratio between carbohydrate and proteins (ratio = carbohydrate/proteins)
    """

    def __init__(self, pos, decay, qte, concentration, ratio):
        diff = abs(1 - ratio)
        if diff == 0:
            res = 0.00001 * concentration
        else:
            res = (1 / diff) * concentration

        super().__init__('Food', pos, res, decay)
        self._quantity = qte
        self._status = True

        self._concentration = concentration
        self._ratio = ratio
        self._quantity = qte

    @property
    def Ratio(self):
        return self._ratio

    @property
    def Concentration(self):
        return self._concentration

    @property
    def State(self):
        return self._status

    def Eat(self):
        """
        Manages the quantity of food eaten by the physarum
        :return:
        """
        self._quantity -= 1
        if self._quantity <= 0: self._status = False
        return {
            "proteine": self._ratio,
            "glucide": 1 - self._ratio,
        }
