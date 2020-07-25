#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-14"

import numpy as np

class History(object):
    """Used to store the simulation
        """

    def __init__(self):
        self._blobs = []
        self._moisture = []
        self._temperature = []
        self._grid = []

    def Export(self):
        pass

    def Import(self):
        pass