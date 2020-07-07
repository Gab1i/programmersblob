import tkinter as tk
import tkinter.font as tkFont

from Emetteur import Emetteur
from World import *
from Blob import *


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.root = tk.Tk()
        self.root.title("The Blob")
        self.root.geometry("{0}x{1}".format(width+300, height))

        self.root.bind('<Return>', self._onEnter)
        self.root.bind('<n>', self._toggleNeighborhood)
        self.root.bind('<Right>', self._upTemp)
        self.root.bind('<Left>', self._downTemp)
        self.root.bind('<Up>', self._upMoisture)
        self.root.bind('<Down>', self._downMoisture)

        self.canvas = tk.Canvas(width=self.width, height=self.height, bd=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT)

        self.menu = tk.Canvas(width=300, height=self.height)
        self.menu.pack()

        #self.nbTickText = tk.Text(self.menu)
        #self.nbTickText.pack()

        self._moisture_world_txt = self.menu.create_text(40, 10, text='Moisture monde', font=('Purisa', 20))
        self._temperature_world_txt = self.menu.create_text(40, 40, text='Temp. monde', font=('Purisa', 20))
        self._moisture_txt = self.menu.create_text(40, 90, text='moisture', font=('Purisa', 20))
        self._food_txt = self.menu.create_text(40, 120, text='Pas faim', font=('Purisa', 20))

        font = tkFont.Font(family="Helvetica", size=36, weight="bold")

        self.canvas.bind('<Button-1>', self._onLeftClick)
        self.canvas.bind('<Button-2>', self._onRightClick)

        self.drawNeighbors = False

        # Initialisation du monde
        self._grid = []
        self.text = []
        self._createWorld(10, 10, 7)

        self.root.mainloop()

    def _upTemp(self, evt):
        self.world._temperature += 1

    def _downTemp(self, evt):
        self.world._temperature -= 1

    def _upMoisture(self, evt):
        self.world._moisture = min(1, self.world._moisture+1)

    def _downMoisture(self, evt):
        self.world._moisture = max(-1, self.world._moisture-1)

    def _onEnter(self, evt):
        self.world.Tick()
        self._drawWorld()
        if self.world._blobs[0]._dead:
            self.menu.itemconfig(self._moisture_txt, text="CACA DEAD")
        else:
            self.menu.itemconfig(self._moisture_world_txt, text=self.world._moisture)
            self.menu.itemconfig(self._moisture_txt, text=self.world._blobs[0]._moisture)

            self.menu.itemconfig(self._temperature_world_txt, text=self.world._temperature)
            self.menu.itemconfig(self._food_txt, text=self.world._blobs[0].GetFoodStatus())
        #self.round()

    def round(self):
        self.world.Tick()

        self._drawWorld()
        self.canvas.after(1, self.round)

    def _onLeftClick(self, evt):
        pos = self._evtToPos(evt)
        self.world.AddEmitter(Food('Flamby', pos, -10, 10, 0.8, 1/5), pos)
        self._drawWorld()

    def _onRightClick(self, evt):
        pos = self._evtToPos(evt)
        #self.world.AddEmitter(Emetteur('Petite Lampe de Bureau qui Perce à travers les feuilles d\'arbre c\'est un peu artistique'
        #                              , pos, -5, 1), pos)
        self.world.AddEmitter(Food('Flanbeurk', pos, -10, 10, 0.5, 1/8), pos)
        self._drawWorld()

    def _evtToPos(self, evt):
        caseWidth = self.width / self.world.col
        caseHeight = self.height / self.world.line
        col = evt.x // caseWidth
        line = evt.y // caseHeight
        pos = int(self.world.coord2pos(line, col))
        return pos

    def _toggleNeighborhood(self, evt):
        self.drawNeighbors = not self.drawNeighbors
        #print(self._blob._neighborhood)

    def _createWorld(self, line, col, pos):
        self.world = World(line, col, pos)
        #self._drawWorld()

        caseWidth = self.width / self.world.col
        caseHeight = self.height / self.world.line

        for c in self.world.grid:
            self._grid.append(self._drawCase(c, caseWidth, caseHeight, '#fefae0'))

    def _drawWorld(self):
        # clear canvas
        # self.canvas.delete("all")

        for c in self.world.grid:
            if c.mucus: color = '#edddd4'
            else: color = '#8cb7b8'

            if self.drawNeighbors and c in self.world._blob._neighborhood:
                color = '#626b3e'

            for a in c.agents:
                if type(a) == Food:
                    if a.name == "Flanbeurk":
                        color = '#698262'
                    else:
                        color = '#b64e3d'
                elif type(a) == Emetteur:
                    if a.name == 'Petite Lampe de Bureau qui Perce à travers les feuilles d\'arbre c\'est un peu artistique': color = '#367077'

            if c.Veine is not None:
                if c.Veine._dessication:
                    color = '#e79540'
                elif c.Veine._dead:
                    color = '#3d3d3d'
                else: color = '#bc6c25'

            if len(c.Spores) > 0:
                color = '#68e3ba'

            self._updateCase(c, color)

    def _updateCase(self, case, color):
        self.canvas.itemconfig(self._grid[case.position], fill=color)

        # show children number of each veine portion
        if case.Veine is not None:
            t = '' #round(case.Veine._size,2)
        else:
            t = ''
        self.canvas.itemconfig(self.text[case.position], text=t)

        # show position of each case
        self.canvas.itemconfig(self.text[case.position], text= round(case._value, 2))

    def _drawCase(self, case, caseWidth, caseHeight, color):
        (yStart, xStart) = case.Coord

        rect = self.canvas.create_rectangle(xStart * caseWidth, yStart * caseHeight, xStart * caseWidth + caseWidth,
                                     yStart * caseHeight + caseHeight, outline="#cccccc", fill=color)

        txt = self.canvas.create_text(xStart * caseWidth + caseWidth/2, yStart * caseHeight + caseHeight/2, text='', font=('Purisa',8))
        self.text.append(txt)
        # AFFICHER LES POSITIONS ET COORDONNEES
        # self.canvas.create_text(xStart * caseWidth + 10, yStart * caseHeight + 10, text=str(case.position))
        # self.canvas.create_text(xStart * caseWidth + 20, yStart * caseHeight + 25, text='({0}, {1})'.format(*case.Coord))


        return rect



