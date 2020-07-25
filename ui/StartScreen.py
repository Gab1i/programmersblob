from tkinter import *
from tkinter import messagebox

from ui.Window import Window


class StartScreen(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title("The blob")
        self.width, self.height = 600, 370

        self.geometry("{0}x{1}".format(self.width, self.height))

        self.positionX = int(self.winfo_screenwidth() / 2 - self.width / 2)
        self.positionY = int(self.winfo_screenheight() / 2 - self.height / 2)

        self.geometry("+{}+{}".format(self.positionX, self.positionY))

        self.l0 = Label(self, text='The Blob', font=("Helvetica", 24), height=2)

        self.l1 = Label(self, text='Attention: Ceci est un logiciel de simulation. Toute expérience doit être réalisé dans un cadre\n'
                                   'professionnel et encadrée du personnel assermenté. L\'entité simulée présente une croissance \n'
                                   'exponentielle. Le physarum polycephalum ne doit pas être pris à la légère. Ne laissez  pas ce \n'
                                   'logiciel entre les mains d\'un binôme de stagiaires inconscients. Faites en bon usage.',
                        pady=5)

        self.l2 = Label(self, text='Paramètres de la simulation', font=("Helvetica", 18))
        self.size = StringVar()
        self.size.set('25')
        self.l3 = Label(self, text='Taille (cases)', width=13, anchor=E)
        self.e1 = Entry(self, state='readonly', textvariable=self.size)

        self.real_size = StringVar()
        self.real_size.set('10')
        self.l4 = Label(self, text='Taille réelle (cm)', width=13, anchor=E)
        self.e2 = Entry(self, state='readonly', textvariable=self.real_size)

        self.time_tick = StringVar()
        self.time_tick.set('1')
        self.l5 = Label(self, text='Temps par tick (h)', width=13, anchor=E)
        self.e3 = Entry(self, state='readonly', textvariable=self.time_tick)

        self.emptyFrame = Frame(self, height=50)
        self.frame = Frame(self)
        self.btn = Button(self.frame, text='Start', command=self.launchSimulation, width=12,  height=2)
        self.btnQuit = Button(self.frame, text='Quit', command=lambda: self.destroy(), width=12, height=2)

        self.config = {}
        self.readConfig()

        self.tutoCanvas = Canvas(self, width=600, height=370, bd=0, highlightthickness=0)
        self._imagetutorial = PhotoImage(file="ui/images/tuto.png")
        self._tuto = self.tutoCanvas.create_image(600 / 2, 370 / 2, image=self._imagetutorial)

        if not self.config['tuto']:
            self.displayTuto()
        else:
            self.makeGrid()

        self.e1.bind('<Key>', lambda e: self._inputText(e, self.size))
        self.e2.bind('<Key>', lambda e: self._inputText(e, self.real_size))
        self.e3.bind('<Key>', lambda e: self._inputText(e, self.time_tick))

        self.win = None

        self.mainloop()

    def displayTuto(self):
        list = self.grid_slaves()
        for l in list:
            l.grid_forget()

        self.tutoCanvas.pack()

        self.tutoCanvas.bind('<Button-1>', self._hideTuto)

    def _hideTuto(self, evt):
        list = self.pack_slaves()
        for l in list:
            l.forget()

        self.makeGrid()

    def _inputText(self, evt, var):
        if evt.keysym == "BackSpace":
            var.set(var.get()[0:-1])
        if evt.char.isdigit():
            var.set(var.get() + evt.char)

    def makeGrid(self):
        self.l0.grid(column=1, row=1, columnspan=2)
        self.l1.grid(column=1, row=2, columnspan=2)
        self.l2.grid(column=1, row=3, columnspan=2)

        self.l3.grid(column=1, row=4)
        self.e1.grid(column=2, row=4)
        self.l4.grid(column=1, row=5)
        self.e2.grid(column=2, row=5)
        self.l5.grid(column=1, row=6)
        self.e3.grid(column=2, row=6)

        self.emptyFrame.grid(column=1, row=7)
        self.frame.grid(column=2, row=8)
        self.btn.grid(column=1, row=1)
        self.btnQuit.grid(column=2, row=1)

    def launchSimulation(self):
        self.withdraw()
        self.win = Window(self, 800, 800, nb_cases=int(self.size.get()), size=int(self.real_size.get()),
                          tick=int(self.time_tick.get()))


    def readConfig(self):
        self.config = {}
        file = open('config.txt', 'r')
        for line in file:
            l = line.split('=')
            self.config[l[0]] = l[1] == '1\n'

    def writeConfig(self):
        file = open('config.txt', 'w')
        file.write('tuto=1')
        file.close()
