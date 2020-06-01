from World import World
from Agent import Food

import tkinter as tk
from Button import Button


class UI:
    def __init__(self, size):
        self.world = World(50)

        self.width = size
        self.height = size

        self.root = tk.Tk()
        self.root.geometry("{0}x{1}".format(size+200, size))

        self.canvas = tk.Canvas(width=self.width, height=self.height, bd=0, highlightthickness=0)
        self.canvas.bind('<Button-1>', self.onClick)
        self.root.bind("<Configure>", self.onResize)
        self.canvas.pack(side=tk.LEFT)

        self.canvas_menu = tk.Canvas(width=200, height=size, highlightthickness=0, bg="#e6e6e6")
        self.canvas_menu.pack(side=tk.LEFT)

        self.button = Button(self.canvas_menu, 'UI/off.png', 20, 20, 'UI/on.png')
        self.canvas_menu.bind('<Button-1>', self.btnClick)
        self.canvas_menu.bind('<Motion>', self.motion)

        self.selected = None

        self.update()

        self.root.mainloop()

    def motion(self, event):
        """
        Method triggered on button click
        """
        self.canvas_menu.config(cursor='arrow')
        if event.x in range(self.button.x[0], self.button.x[1]) and event.y in range(self.button.y[0], self.button.y[1]):
            self.canvas_menu.config(cursor='hand')

    def btnClick(self, event):
        """
        Method triggered on mouse move
        """
        if self.button.x[0] < event.x < self.button.x[1] and self.button.y[0] < event.y < self.button.y[1]:
            self.button.toggle()

    def update(self):
        self.canvas.delete("all")
        self.world.tick()

        for i in range(self.world.size ** 2):
            if self.world.grid[i].isAgent():
                color = 'red'
            else:
                color = 'white'
            self.drawCase(i, color)

        #self.drawField('food')

        if self.selected != None: self.drawNeighborhood(self.selected[0], self.selected[1])

    def drawCase(self, i, color):
        (yStart, xStart) = self.world.pos2coord(i)
        caseWidth = self.width / self.world.size
        caseHeight = self.height / self.world.size

        self.canvas.create_rectangle(xStart * caseWidth, yStart * caseHeight, xStart * caseWidth + caseWidth,
                                     yStart * caseHeight + caseHeight, outline="#cccccc", fill=color)

    def onClick(self, e):
        caseWidth = self.width / self.world.size
        col = e.x // caseWidth
        line = e.y // caseWidth
        pos = int(self.world.coord2pos(line, col))

        self.world.grid[pos].agent = True

        self.world.agents.append(Food('Champignon', line, col))
        self.selected = (line, col)

        self.update()

    def onResize(self, e):
        pass
        """self.width = e.width
        self.height = e.height
        print("{0}x{1}".format(e.width, e.height))
        self.update()"""

    def drawField(self, posAgent):
        pass

    def drawField(self, typeField):
        for i in range(self.world.size ** 2):
            if typeField in self.world.grid[i].fields:
                v = self.world.grid[i].fields[typeField]
                maxColor = self.world.grid[i].maxFields[typeField][1]
                color = int(v / maxColor * 255)

                rgb = (color, 0, 0)
                color = "#%02x%02x%02x" % rgb
                self.drawCase(i, color)

    def drawNeighborhood(self, line, col):
        for i in range(1, 10):
            neighbors = self.world.neighbor(line, col, i)

            color = int(i / 10 * 255)
            rgb = (0, color, 0)
            color = "#%02x%02x%02x" % rgb
            for n in neighbors:
                self.drawCase(n, color)
