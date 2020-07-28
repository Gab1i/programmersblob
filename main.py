#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Simon Audrix & Gabriel Nativel-Fontaine"
__date__ = "20-07-14"
__usage__ = "Physarum polycephalum simulation"
__version__ = "2.0"
__update__ = "20-07-24"

from ui.StartScreen import StartScreen
from tkinter import *
from tkinter import messagebox

if __name__ == "__main__":
    try:
        splash = StartScreen()
    except:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Erreur inconnue",
                             "Ooops il semble qu'un problème soit survenu ! Le programme va être fermé.")
