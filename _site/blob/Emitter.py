#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-14"


class Emitter:
    """An emitter emits a field in the world which can be detected by physarum polycephalum
    :param string name: name identifying the emitter
    :param int pos: position of the emitter
    :param int power: power of the field
    :param int decay: evolution of the field with distance
    """
    def __init__(self, name, pos, power, decay):
        self._name = name
        self._power = power
        self._decay = decay
        self._position = pos
        self._distance = int(abs(power) / abs(decay))

    @property
    def Position(self):
        return self._position

    @property
    def Name(self):
        return self._name

    @property
    def Power(self):
        return self._power

    @property
    def Decay(self):
        return self._decay

    @property
    def Distance(self):
        return self._distance
