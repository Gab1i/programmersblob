from World import World
from Agent import Food

import tkinter as tk

class UI:
    def __init__(self, size):
        self.world = World(50)
        self.windowSize = size
        self.root = tk.Tk()
        self.root.geometry("{0}x{0}".format(size))
        self.canvas = tk.Canvas(width=self.windowSize, height=self.windowSize)
        # self.update()

        self.canvas.bind('<Button-1>', self.onClick)
        self.canvas.pack()

        self.root.mainloop()

    def update(self):
        self.canvas.delete("all")
        self.world.tick()

        for i in range(self.world.size ** 2):
            if self.world.grid[i].isAgent():
                color = 'red'
            else:
                color = 'white'
            self.drawCase(i, color)

        self.drawField('food')

    def drawCase(self, i, color):
        (xStart, yStart) = self.world.pos2coord(i)
        caseWidth = self.windowSize / self.world.size
        self.canvas.create_rectangle(xStart * caseWidth, yStart * caseWidth, xStart * caseWidth + caseWidth,
                                     yStart * caseWidth + caseWidth, outline="black", fill=color)

    def onClick(self, e):
        caseWidth = self.windowSize / self.world.size
        col = e.x // caseWidth
        line = e.y // caseWidth
        pos = int(self.world.coord2pos(col, line))
        print(pos)
        self.world.grid[pos].agent = True

        self.world.agents.append(Food('Champignon', line, col))

        self.update()

    def drawField(self, posAgent):
        pass

    def drawField(self, typeField):
        for i in range(self.world.size ** 2):
            if typeField in self.world.grid[i].fields:
                v = self.world.grid[i].fields[typeField]
                color = int(v / 100 * 255)
                print(color)
                rgb = (color, 0, 0)
                color = "#%02x%02x%02x" % rgb
                self.drawCase(i, color)

