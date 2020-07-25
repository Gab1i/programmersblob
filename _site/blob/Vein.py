#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-14"


class Vein(object):
    """The Vein object is an object allowing manipulations of sub-elements of the physarum polycephalum
        :param Blob blob: the parent blob
        :param Case case : box on which is the vein
        :param Vein parent: Vein that generated this vein
        """

    def __init__(self, blob, case, parent):
        self._blob = blob
        self._case = case
        self._parent = parent
        self._children = []

        if self._parent is not None:
            self._parent._children.append(self)

    @property
    def isExtremity(self):
        """
        Return true if the vein is an extremity
        :return: bool
        """
        return len(self._children) == 0 or (self._parent is None and len(self._children) == 1)

    @property
    def Blob(self):
        return self._blob

    @property
    def Case(self):
        return self._case

    def Kill(self):
        """
        Kill the vein by removing its reference from its parent and its children
        """
        if self._parent is not None:
            self._parent._children.remove(self)

        for child in self._children:
            child._parent = None
