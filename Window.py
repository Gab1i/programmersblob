import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

from Emetteur import Emetteur
from World import *
from Blob import *
from tkinter.filedialog import *


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.root = tk.Tk()
        self.root.title("The Blob")
        self.root.geometry("{0}x{1}".format(width + 300, height))

        self.foodConcentration = tk.DoubleVar(self.root, 1)
        self.foodRatio = tk.DoubleVar(self.root, 0.5)

        self.root.bind('<Return>', self._onEnter)
        self.root.bind('<p>', self._rrrrr)
        self.root.bind('<n>', self._toggleNeighborhood)
        self.root.bind('<Right>', self._upTemp)
        self.root.bind('<Left>', self._downTemp)
        self.root.bind('<Up>', self._upMoisture)
        self.root.bind('<Down>', self._downMoisture)

        self.canvas = tk.Canvas(width=self.width, height=self.height, bd=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT)

        self.menu = tk.Frame(width=300, height=self.height)
        self.menu.pack(side=tk.TOP)

        self._slider_temperature = tk.Scale(self.menu, orient='horizontal', from_=-6, to=40, resolution=1,
                                            tickinterval=10,
                                            length=240, label='Température (en °C)', command=self.setTemp)
        self._slider_temperature.set(27)
        self._slider_temperature.pack()

        self._slider_humidite = tk.Scale(self.menu, orient='horizontal', from_=0, to=100, resolution=1,
                                         tickinterval=100,
                                         length=240, label='Humidité (%)', command=self.setMoisture)
        self._slider_humidite.set(60)
        self._slider_humidite.pack()

        self._frame1 = tk.Frame(self.menu)

        tk.Label(self._frame1, text='h/tick: ', anchor=tk.W, justify=tk.LEFT).grid(column=1, row=1)
        self._hour_tick_txt = tk.Label(self._frame1, text='')
        self._hour_tick_txt.grid(column=2, row=1)

        tk.Label(self._frame1, text='Ellapsed time: ', anchor=tk.W, justify=tk.LEFT).grid(column=1, row=2)
        self._time_txt = tk.Label(self._frame1, text='')
        self._time_txt.grid(column=2, row=2)

        var1 = tk.IntVar()
        self._boxChamp = tk.Checkbutton(self._frame1, variable=var1).grid(column=2, row=5)
        tk.Label(self._frame1, text='Afficher champ: ', anchor=tk.W, justify=tk.LEFT).grid(column=1, row=5)


        tk.Label(self._frame1, text='Nourriture: ', justify=tk.LEFT).grid(column=1, row=6)

        self._slider_bouffe = tk.Scale(self._frame1, orient='horizontal', from_=0, to=1, resolution=0.1,
                                       tickinterval=1, label='Ratio',
                                       length=240, variable=self.foodRatio).grid(column=1, row=8, columnspan=2)

        self._slider_bouffe2 = tk.Scale(self._frame1, orient='horizontal', from_=0, to=1, resolution=0.1,
                                        tickinterval=1, label='Concentration',
                                        length=240, variable=self.foodConcentration).grid(column=1, row=10, columnspan=2)

        self.foodValue = tk.StringVar()
        self.foodValue.set("1")
        self.foodText = tk.Entry(self._frame1, state="readonly", textvariable=self.foodValue)

        self.original = self.foodText.cget("highlightbackground")

        tk.Label(self._frame1, text='Quantité: ', justify=tk.LEFT).grid(column=1, row=11)
        self.foodText.grid(column=2, row=11)
        #self.foodText.setT

        #self.foodValue = "1"

        self._frame1.pack(anchor=tk.W)

        # self._frame2 = tk.Frame(self.menu, background='red').pack()
        # tk.Label(self._frame2, text='roger: ', anchor=tk.NW).pack()
        # self._hour_tick_txt = tk.Label(self._frame2, text='13').pack()

        # self.nbTickText = tk.Text(self.menu)
        # self.nbTickText.pack()

        font = tkFont.Font(family="Helvetica", size=36, weight="bold")

        self.canvas.bind('<Button-1>', self._onLeftClick)
        self.canvas.bind('<Button-2>', self._onRightClick)

        self.foodText.bind('<Key>', self._inputText)

        self.drawNeighbors = False

        # Initialisation du monde
        self._grid = []
        self.text = []
        self._createWorld(25, 25, 5)

        self.root.mainloop()

    def _inputText(self, evt):
        if evt.keysym == "BackSpace":
            self.foodValue.set(self.foodValue.get()[0:-1])
        if evt.char.isdigit():
            self.foodValue.set(self.foodValue.get() + evt.char)

        if self.foodValue.get() == "":
            self.foodText["highlightbackground"] = "#ff0000"
        else:
            self.foodText["highlightbackground"] = self.original


    def formatTime(self, hours):
        nbJours = hours // 24

        if nbJours == 0:
            return "{0}h".format(hours)

        return "{0}d {1}h".format(nbJours, hours%24)

    def setTemp(self, temp):
        temp = int(temp)
        self.world._temperature = temp

    def setMoisture(self, m):
        m = int(m)
        if 0 <= m <= 46:
            self.world._moisture = -1
        elif 47 <= m <= 80:
            self.world._moisture = 0
        else:
            self.world._moisture = 1

    def _upTemp(self, evt):
        self.world._temperature += 1

    def _downTemp(self, evt):
        self.world._temperature -= 1

    def _upMoisture(self, evt):
        self.world._moisture = min(1, self.world._moisture + 1)

    def _downMoisture(self, evt):
        self.world._moisture = max(-1, self.world._moisture - 1)

    def _onEnter(self, evt):
        self.world.Tick()

        self._hour_tick_txt['text'] = self.world.nombreHeureParTick
        self._time_txt['text'] = self.formatTime(self.world.ellapsedTime)
        self._drawWorld()

        # self.round()

    def _rrrrr(self, evt):
        self.round()

    def round(self):
        self.world.Tick()

        self._drawWorld()
        self.canvas.after(1, self.round)

    def _onLeftClick(self, evt):
        pos = self._evtToPos(evt)
        self.foodText["highlightbackground"] = self.original

        if self.foodValue.get() == "":
            self.foodText.bell()
            messagebox.showerror("Quantité de nourriture", "Veuillez entrer une quantité de nourriture valide s'il-vous-plait !")
            self.foodText["highlightbackground"] = "#ff0000"

        else:
            self.world.AddEmitter(
                Food('Flamby', pos, -100, int(self.foodValue.get()), self.foodConcentration.get(), self.foodRatio.get()),
                pos)
            self._drawWorld()

    def _onRightClick(self, evt):
        pos = self._evtToPos(evt)

        self.world.grid[pos].Sel = True
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
        # print(self._blob._neighborhood)

    def _createWorld(self, line, col, pos):
        self.world = World(line, col, pos)
        # self._drawWorld()

        caseWidth = self.width / self.world.col
        caseHeight = self.height / self.world.line

        for c in self.world.grid:
            self._grid.append(self._drawCase(c, caseWidth, caseHeight, '#fefae0'))

    def _drawWorld(self):
        # clear canvas
        # self.canvas.delete("all")

        for c in self.world.grid:
            if c.mucus:
                color = '#edddd4'
            else:
                color = '#8cb7b8'

            if c.Sel:
                color = '#34ebb4'

            if self.drawNeighbors and c in self.world._blob._neighborhood:
                color = '#626b3e'

            for a in c.agents:
                if type(a) == Food:
                    color = self.getColor(a)
                elif type(a) == Emetteur:
                    if a.name == 'Petite Lampe de Bureau qui Perce à travers les feuilles d\'arbre c\'est un peu artistique': color = '#367077'

            if c.Veine is not None:
                if c.Veine._dessication:
                    color = '#e79540'
                elif c.Veine._dead:
                    color = '#3d3d3d'
                else:
                    color = '#bc6c25'

                if c.Veine.isExtremity: color = '#6C0277'

            if len(c.Spores) > 0:
                color = self.getColorSexe(c.Spores[0]._sexe)
                #color = '#68e3ba'

            self._updateCase(c, color)

    def _updateCase(self, case, color):
        self.canvas.itemconfig(self._grid[case.position], fill=color)

        # show children number of each veine portion
        #if case.Veine is not None:
        #    t = ''  # round(case.Veine._size,2)
        #else:
        #    t = ''
        #self.canvas.itemconfig(self.text[case.position], text=t)

        # show position of each case
        #self.canvas.itemconfig(self.text[case.position], text=round(case._value, 2))

    def _drawCase(self, case, caseWidth, caseHeight, color):
        (yStart, xStart) = case.Coord

        rect = self.canvas.create_rectangle(xStart * caseWidth, yStart * caseHeight, xStart * caseWidth + caseWidth,
                                            yStart * caseHeight + caseHeight, outline="#cccccc", fill=color)

        txt = self.canvas.create_text(xStart * caseWidth + caseWidth / 2, yStart * caseHeight + caseHeight / 2, text='',
                                      font=('Purisa', 8))
        self.text.append(txt)
        # AFFICHER LES POSITIONS ET COORDONNEES
        # self.canvas.create_text(xStart * caseWidth + 10, yStart * caseHeight + 10, text=str(case.position))
        # self.canvas.create_text(xStart * caseWidth + 20, yStart * caseHeight + 25, text='({0}, {1})'.format(*case.Coord))

        return rect

    def getColorSexe(self, a):
        c = int(a / 720 * 255)
        return '#%02x%02x%02x' % (c, 229, 52)

    def getColor(self, a):
        hue = a.ratio * 100
        saturation = a.concentration
        brightness = 1

        return '#%02x%02x%02x' % self.hsv2rgb(round(hue), saturation, brightness)

    def hsv2rgb(self, h, s, v):

        C = v * s
        X = C * (1 - (abs((h/60) % 2 - 1)))
        m = v - C

        if 0 <= h < 60:
            r2 = C
            g2 = X
            b2 = 0
        elif 60 <= h < 120:
            r2 = X
            g2 = C
            b2 = 0
        elif 120 <= h < 180:
            r2 = 0
            g2 = C
            b2 = X
        elif 180 <= h < 240:
            r2 = 0
            g2 = X
            b2 = C
        elif 240 <= h < 300:
            r2 = X
            g2 = 0
            b2 = C
        elif 300 <= h <= 360:
            r2 = C
            g2 = 0
            b2 = X
        return (round((r2 + m) * 255), round((g2 + m) * 255), round((b2 + m) * 255))
