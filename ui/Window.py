from tkinter import *
from tkinter import messagebox

from blob import Food, Emitter, Vein
from blob.World import World


class Window(Toplevel):
    def __init__(self, menu, width, height, nb_cases=25, size=10, tick=1):
        Toplevel.__init__(self)
        self.config = {}
        self.readConfig()
        self.title("The blob")

        # set size
        self.width, self.height = width, height
        self.geometry("{0}x{1}".format(width + 300, height))

        # set window position
        self.positionX = int(self.winfo_screenwidth() / 2 - (self.width + 300) / 2)
        self.positionY = int(self.winfo_screenheight() / 2 - self.height / 2)
        self.geometry("+{}+{}".format(self.positionX, self.positionY))

        # Building main window
        self.canvas = Canvas(self, width=self.width, height=self.height, bd=0, highlightthickness=0)

        self.menu = Frame(self, width=300, height=self.height)

        # Building menu
        # =============== LEGENDE ============
        self._legendeTitle = Label(self.menu, text='LEGENDE', font=("Helvetica", 13, 'bold'))

        self._legendeFrame = Frame(self.menu)
        self._canvasLegende1 = Canvas(self._legendeFrame, width=15, height=15, background=self.config['color_blob'])
        self._labelLegende1 = Label(self._legendeFrame, text='Blob', width=10, anchor=W)

        self._canvasLegende2 = Canvas(self._legendeFrame, width=15, height=15, background=self.config['color_sclerote'])
        self._labelLegende2 = Label(self._legendeFrame, text='Sclérote', anchor=W, width=10)

        self._canvasLegende3 = Canvas(self._legendeFrame, width=15, height=15, background=self.config['color_spore'])
        self._labelLegende3 = Label(self._legendeFrame, text='Spores', width=10, anchor=W)

        self._canvasLegende4 = Canvas(self._legendeFrame, width=13, height=13, background=self.config['color_sel'],
                                      highlightthickness=1, highlightbackground="gray")
        self._labelLegende4 = Label(self._legendeFrame, text='Sel', width=10, anchor=W)

        self._canvasLegende5 = Canvas(self._legendeFrame, width=15, height=15, background=self.config['color_light'])
        self._labelLegende5 = Label(self._legendeFrame, text='Point lumineux', width=10, anchor=W)

        self._canvasLegende7 = Canvas(self._legendeFrame, width=15, height=15, background=self.config['color_mucus'])
        self._labelLegende7 = Label(self._legendeFrame, text='Mucus', width=10, anchor=W)

        self._canvasLegende6 = Canvas(self._legendeFrame, width=150, height=15)
        self._imagegradient = PhotoImage(file="ui/images/gradient_food.png")
        self._tuto = self._canvasLegende6.create_image(150 / 2, 15 / 2, image=self._imagegradient)
        self._labelLegende6 = Label(self._legendeFrame, text='Nourriture', width=10, anchor=W)

        self.hr = Canvas(self.menu, width=290, height=17, bd=0, highlightthickness=0)
        self.hr.create_line(0, 5, 289, 5, fill='#b8b8b8')

        # =============== NOURRITURE ============

        self._foodTitle = Label(self.menu, text='NOURRITURE', anchor=W, justify=CENTER, font=("Helvetica", 13, 'bold'))

        self._frame1 = Frame(self.menu)

        self.foodRatio = DoubleVar()
        self._scale1 = Scale(self._frame1, orient='horizontal', from_=0, to=1, resolution=0.1, tickinterval=1,
                             label='Ratio', troughcolor="#0000ff",
                             length=240, variable=self.foodRatio, command=self._colorScale)
        self._scale1.set(0.5)

        self.foodConcentration = DoubleVar()
        self._scale2 = Scale(self._frame1, orient='horizontal', from_=0.1, to=1, resolution=0.1, tickinterval=1,
                             label='Concentration',
                             length=240, variable=self.foodConcentration, command=self._colorScale2)
        self._scale2.set(1.0)

        self.foodValue = StringVar()
        self.foodValue.set("1")
        self._l6 = Label(self._frame1, text='Quantité: ', justify=LEFT)
        self.foodText = Entry(self._frame1, state="readonly", textvariable=self.foodValue)

        self.originalColor = self.foodText.cget("highlightbackground")

        self.hr2 = Canvas(self.menu, width=290, height=17, bd=0, highlightthickness=0)
        self.hr2.create_line(0, 5, 289, 5, fill='#b8b8b8')
        self._l1 = Label(self.menu, text='ENVIRONNEMENT', anchor=W, justify=CENTER, font=("Helvetica", 13, 'bold'))

        self._slider_temperature = Scale(self.menu, orient='horizontal', from_=-6, to=40, resolution=1, tickinterval=10,
                                         length=240, label='Température (en °C)', command=self._setTemperature)
        self._slider_temperature.set(27)

        self._slider_humidite = Scale(self.menu, orient='horizontal', from_=0, to=100, resolution=1, tickinterval=100,
                                      length=240, label='Humidité (%)', command=self._setMoisture)
        self._slider_humidite.set(60)

        self.hr3 = Canvas(self.menu, width=290, height=17, bd=0, highlightthickness=0)
        self.hr3.create_line(0, 5, 289, 5, fill='#b8b8b8')
        self._titleGlobal = Label(self.menu, text="INFORMATIONS", font=("Helvetica", 13, 'bold'))

        self._frame2 = Frame(self.menu)
        self._l2 = Label(self._frame2, text='h/tick: ', anchor=W, width=12)
        self._hour_tick_txt = Label(self._frame2, text='', anchor=W, width=18, font=("Helvetica", 12, 'bold'))

        self._l3 = Label(self._frame2, text='Ellapsed time: ', anchor=W, width=12)
        self._time_txt = Label(self._frame2, text='0h', anchor=W, width=18, font=("Helvetica", 12, 'bold'))

        checkBoxChamp = IntVar()
        self._checkbox = Checkbutton(self._frame2, variable=checkBoxChamp)
        self._l4 = Label(self._frame2, text='Afficher champ: ', anchor=W, justify=LEFT)

        self.hr4 = Canvas(self.menu, width=290, height=17, bd=0, highlightthickness=0)
        self.hr4.create_line(0, 5, 289, 5, fill='#b8b8b8')
        self._titleControl = Label(self.menu, text="CONTROLES", font=("Helvetica", 13, 'bold'))
        self._frame3 = Frame(self.menu)

        self._clickVar = IntVar()
        self._rdbtn1 = Radiobutton(self._frame3, variable=self._clickVar, text="Blob", value=0, indicatoron=0, width=7,
                                   selectcolor=self.config['color_blob'])
        self._rdbtn2 = Radiobutton(self._frame3, variable=self._clickVar, text="Nourriture", value=1, indicatoron=0,
                                   width=7, selectcolor='#00ff00')
        self._rdbtn3 = Radiobutton(self._frame3, variable=self._clickVar, text="Sel", value=2, indicatoron=0, width=7,
                                   selectcolor=self.config['color_sel'])
        self._rdbtn4 = Radiobutton(self._frame3, variable=self._clickVar, text="Lumière", value=3, indicatoron=0,
                                   width=7, selectcolor=self.config['color_light'])

        self._frame4 = Frame(self.menu)
        self._frameVide = Frame(self.menu, height=20)
        self._btnStart = Button(self._frame4, text="Start", command=self._toggleSimulation, width=7, height=2)
        self._btnNext = Button(self._frame4, text="Next", command=self._step, width=7, height=2)
        self._btnBack = Button(self._frame4, text="Back", command=self._back, width=7, height=2)

        self._imagetutorial = [
            "ui/images/tuto_1.png",
            "ui/images/tuto_2.png",
            "ui/images/tuto_3.png",
            "ui/images/tuto_5.png",
            "ui/images/tuto_6.png",
            "ui/images/tuto_7.png",
            "ui/images/tuto_8.png"
        ]
        self._tutoCanvas = Canvas(self, width=1100, height=800, bd=0, highlightthickness=0)
        self._image = PhotoImage(file=self._imagetutorial[0])

        self._step_tuto = 0
        self._tuto = self._tutoCanvas.create_image(1100 / 2, 800 / 2, image=self._image)

        # -----
        self._displayField = False

        # Some bindings
        self.canvas.bind('<Button-1>', self._onLeftClick)
        self.canvas.bind('<Button-2>', self._onRightClick)
        self.canvas.bind('<Motion>', self._motion)

        self.foodText.bind('<Key>', self._inputText)

        # initialize the simulation
        self._grid = []
        self.text = []

        if self.config['tuto'] == '0':
            self._displayTuto()
        else:
            self._setupInterface()

        self._createWorld(nb_cases, size, tick)

        self._loop = None

        self._info = []

        self._menu = menu
        self.protocol("WM_DELETE_WINDOW", self._closeWindow)
        self.lift()
        self.attributes("-topmost", 1)

        menuBar = Menu(self)
        self['menu'] = menuBar

        sousMenu = Menu(menuBar)
        menuBar.add_cascade(label='Aide', menu=sousMenu)
        sousMenu.add_command(label='Tutoriel', command=self._menuTutoriel)

        self.mainloop()

    def _motion(self, event):
        x, y = event.x, event.y
        self._displayInfo(self._evtToPos(event), x, y)

    def _displayInfo(self, pos, x, y):
        for w in self._info:
            self.canvas.delete(w)

        width = 110
        height = 130

        if x > 720:
            start = x - width + 10
        else:
            start = x + 10

        if y > 700:
            startY = y - width
        else:
            startY = y

        if self.world.Grid[pos].Vein is not None:
            blob = self.world.Grid[pos].Vein.Blob
            self._info.append(self.canvas.create_rectangle(start, startY, start + width, startY + height,
                                                      outline="#ffffff", fill='#000000'))
            self._info.append(self.canvas.create_text(start+10, startY+15, text='id: {0}'.format(blob.Id),
                                                      fill='white', anchor=W))
            self._info.append(self.canvas.create_text(start + 10, startY + 55, text='Age: {0}'.format(blob.Age),
                                                      fill='white', anchor=W))
            self._info.append(self.canvas.create_text(start + 10, startY + 75, text='Sexe: {0}'.format(blob._sex),
                                                      fill='white', anchor=W))
            self._info.append(self.canvas.create_text(start + 10, startY + 95, text='Taille: {0}'.format(len(blob._veins)),
                                                      fill='white', anchor=W))
            if blob.isDead:
                etat = "mort"
            elif blob.isSclerote:
                etat = "sclérote"
            else:
                etat = blob.FoodState()
            self._info.append(self.canvas.create_text(start+10, startY+35, text='Etat: {0}'.format(etat),
                                                      fill='white', anchor=W))


        # add an empty string for some display
        # txt = self.canvas.create_text(xStart * caseWidth + caseWidth / 2, yStart * caseHeight + caseHeight / 2, text='')


    def _displayTuto(self):
        listGrid = self.grid_slaves()
        listPack = self.pack_slaves()
        for l in listGrid:
            l.grid_forget()
        for l in listPack:
            l.forget()

        self._tutoCanvas.pack()
        self._tutoCanvas.bind('<Button-1>', self._loopTuto)

    def _loopTuto(self, evt):
        if self._step_tuto == len(self._imagetutorial) - 1:
            self._hideTuto()
        else:
            self._step_tuto += 1
            self._image.configure(file=self._imagetutorial[self._step_tuto])

    def _hideTuto(self):
        list = self.pack_slaves()
        for l in list:
            l.forget()

        if self.config['tuto'] == '0':
            self._writeConfig()

        self._setupInterface()

    def _menuTutoriel(self):
        self._displayTuto()

    def _colorScale(self, evt):
        self._scale1['troughcolor'] = self._getColor(self.foodRatio.get(), self.foodConcentration.get())

    def _colorScale2(self, evt):
        c = 255 - int(self.foodConcentration.get() * 255)
        self._scale1['troughcolor'] = self._getColor(self.foodRatio.get(), self.foodConcentration.get())
        self._scale2['troughcolor'] = '#%02x%02x%02x' % (c, c, c)

    def _toggleSimulation(self):
        if self._btnStart['text'] == 'Start':
            self._btnStart['text'] = 'Pause'
            self._loopSimulation()
        else:
            self._btnStart['text'] = 'Start'
            self.canvas.after_cancel(self._loop)

    def _loopSimulation(self):
        self._tickSimulation()
        self._loop = self.canvas.after(100, self._loopSimulation)

    def _tickSimulation(self):
        self.world.Tick()

        self._time_txt['text'] = self._formatTime(self.world.ElapsedTime)
        self._drawWorld()

    def _formatTime(self, hours):
        nbJours = hours // 24

        if nbJours == 0:
            return "{0}h".format(hours)

        return "{0}d {1}h".format(nbJours, hours % 24)

    def _step(self):
        self._tickSimulation()

    def _back(self):
        pass

    def _closeWindow(self):
        self._menu.update()
        self._menu.deiconify()
        self.destroy()

    def _createWorld(self, nb_cases, size, tick):
        self.world = World(nb_cases=nb_cases, total_size=size, tick=tick)
        self._hour_tick_txt['text'] = self.world.TimeTick

        caseWidth = self.width / nb_cases
        caseHeight = self.height / nb_cases

        for c in self.world.Grid:
            self._grid.append(self._drawCase(c, caseWidth, caseHeight, self.config['color_world']))

    def _setupInterface(self):
        self.canvas.pack(side=LEFT)
        self.menu.pack(side=TOP)

        self._legendeTitle.pack()
        self._legendeFrame.pack()

        self.hr.pack()

        self._canvasLegende1.grid(column=1, row=1, sticky=W)
        self._labelLegende1.grid(column=2, row=1, sticky=W)
        self._canvasLegende2.grid(column=1, row=2, sticky=W)
        self._labelLegende2.grid(column=2, row=2, sticky=W)
        self._canvasLegende3.grid(column=3, row=1, sticky=W)
        self._labelLegende3.grid(column=4, row=1, sticky=W)

        self._canvasLegende7.grid(column=3, row=2, sticky=W)
        self._labelLegende7.grid(column=4, row=2, sticky=W)

        self._canvasLegende5.grid(column=1, row=5, sticky=W)
        self._labelLegende5.grid(column=2, row=5, sticky=W)
        self._canvasLegende4.grid(column=3, row=5, sticky=W)
        self._labelLegende4.grid(column=4, row=5, sticky=W)

        self._canvasLegende6.grid(column=1, row=7, columnspan=4, sticky=W)
        self._labelLegende6.grid(column=1, row=6, columnspan=4, sticky=W)

        self._foodTitle.pack()
        self._frame1.pack()
        self._scale1.grid(column=1, row=2, columnspan=2)
        self._scale2.grid(column=1, row=3, columnspan=2)
        self._l6.grid(column=1, row=4)
        self.foodText.grid(column=2, row=4)

        self.hr2.pack()

        self._l1.pack()
        self._slider_temperature.pack()
        self._slider_humidite.pack()

        self.hr3.pack()
        self._titleGlobal.pack()
        self._frame2.pack()

        self._l2.grid(column=1, row=2)
        self._hour_tick_txt.grid(column=2, row=2)

        self._l3.grid(column=1, row=3)
        self._time_txt.grid(column=2, row=3)

        self.hr4.pack()
        self._titleControl.pack()
        self._frame3.pack()
        self._rdbtn1.grid(column=1, row=1)
        self._rdbtn2.grid(column=2, row=1)
        self._rdbtn3.grid(column=1, row=2)
        self._rdbtn4.grid(column=2, row=2)

        self._frameVide.pack()
        self._frame4.pack()
        self._btnStart.grid(column=1, row=1)
        self._btnNext.grid(column=2, row=1)
        self._btnBack.grid(column=3, row=1)

    def _setTemperature(self, value):
        self.world.SetTemperature(int(value))

    def _setMoisture(self, value):
        m = int(value)
        self.world.SetMoisture(m)

    def _evtToPos(self, evt):
        caseWidth = self.width / self.world.Size
        caseHeight = self.height / self.world.Size
        col = evt.x // caseWidth
        line = evt.y // caseHeight

        pos = int(self.world.Coord2pos(line, col))
        return pos

    def _onLeftClick(self, evt):
        pos = self._evtToPos(evt)
        value = self._clickVar.get()

        if value == 0:  # blob
            self._addBlob(pos)
        elif value == 1:  # nourriture
            self._addFood(pos)
        elif value == 2:  # sel
            self._addSalt(pos)
        elif value == 3:  # lumière
            self._addLight(pos)
        else:
            pass

    def _addBlob(self, pos):
        self.world.AddBlob(pos)
        self._drawWorld()

    def _addSalt(self, pos):
        self.world.AddSalt(pos)
        self._drawWorld()

    def _addLight(self, pos):
        self.world.AddLight(pos)
        self._drawWorld()

    def _addFood(self, pos):
        self.foodText["highlightbackground"] = self.originalColor

        if self.foodValue.get() == "":
            self.foodText.bell()
            messagebox.showerror("Quantité de nourriture",
                                 "Veuillez entrer une quantité de nourriture valide s'il-vous-plait !")
            self.foodText["highlightbackground"] = "#ff0000"
        else:
            self.world.AddFood(int(self.foodValue.get()), self.foodConcentration.get(), self.foodRatio.get(), pos)
            self._drawWorld()

    def _onRightClick(self, evt):
        pass

    def _inputText(self, evt):
        if evt.keysym == "BackSpace":
            self.foodValue.set(self.foodValue.get()[0:-1])
        if evt.char.isdigit():
            self.foodValue.set(self.foodValue.get() + evt.char)

        if self.foodValue.get() == "":
            self.foodText["highlightbackground"] = "#ff0000"
        else:
            self.foodText["highlightbackground"] = self.originalColor

    def _drawWorld(self):
        for c in self.world.Grid:
            if c.Updated:
                color = self.config['color_world']
                text = None

                for agent in c.Agents:
                    if type(agent) == Food:
                        color = self._getColor(agent.Ratio, agent.Concentration)
                    elif type(agent) == Emitter and agent.Name == 'Light':
                        color = self.config['color_light']

                if c.Vein is not None:
                    if c.Vein.Blob.isDead:
                        color = self.config['color_dead']
                    elif c.Vein.Blob.isSclerote:
                        color = self.config['color_sclerote']
                    else:
                        color = self.config['color_blob']
                elif c.Salt:
                    color = self.config['color_sel']
                elif len(c.Spores) > 0:
                    color = self.config['color_spore']
                    text = c.Spores[0].Sex
                elif c.Mucus:
                    color = self.config['color_mucus']

                self._updateCase(c, color, text)

    def _drawCase(self, case, caseWidth, caseHeight, color):
        (yStart, xStart) = case.Coord

        rect = self.canvas.create_rectangle(xStart * caseWidth, yStart * caseHeight, xStart * caseWidth + caseWidth,
                                            yStart * caseHeight + caseHeight, outline="#ffffff", fill=color)

        # add an empty string for some display
        txt = self.canvas.create_text(xStart * caseWidth + caseWidth / 2, yStart * caseHeight + caseHeight / 2, text='')
        self.text.append(txt)

        return rect

    def _updateCase(self, case, color, text=None):
        # case.FinishUpdate()
        self.canvas.itemconfig(self._grid[case.Position], fill=color)
        if text is None:
            self.canvas.itemconfig(self.text[case.Position], text='')
        else:
            self.canvas.itemconfig(self.text[case.Position], text=self._getEmoji(32))

        # show field value
        if self._displayField:
            self.canvas.itemconfig(self.text[case.Position], text=round(case.Field, 1))

    def readConfig(self):
        self.config = {}
        file = open('config.txt', 'r')
        for line in file:
            l = line.split('=')
            self.config[l[0]] = l[1][0:-1]

    def _getColor(self, ratio, concentration):
        hue = (ratio * (280 - 180)) + 180
        saturation = concentration
        brightness = 1

        return '#%02x%02x%02x' % self._hsv2rgb(round(hue), saturation, brightness)

    def _hsv2rgb(self, h, s, v):
        C = v * s
        X = C * (1 - (abs((h / 60) % 2 - 1)))
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

    def _writeConfig(self):
        with open('config.txt') as f:
            lines = f.readlines()

        lines[0] = 'tuto=1\n'

        with open('config.txt', 'w') as f:
            f.writelines(lines)

    def _getEmoji(self, idx):
        emoji = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '☺️', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰',
                 '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒',
                 '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬',
                 '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑',
                 '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧',
                 '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖',
                 '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
        return emoji[idx][0:1]
