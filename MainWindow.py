from tkinter import *
from CustomButton import CustomButton
from CustomCanvas import CustomCanvas


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Der Blob')
        self.width, self.height = 800, 600

        self.positionX = int(self.winfo_screenwidth() / 2 - self.width / 2)
        self.positionY = int(self.winfo_screenheight() / 2 - self.height / 2)

        self.geometry("+{}+{}".format(self.positionX, self.positionY))

        self.leftCanvas = CustomCanvas(self, width=self.width, height=self.height, bg='white')
        self.leftCanvas.pack(side=LEFT)

        self.rightCanvas = CustomCanvas(self, width=self.width, height=self.height, bg='blue')
        # self.leftCanvas.pack(side=LEFT)

        self.wm_overrideredirect(True)
        self.update_idletasks()
        self.lift()
        self.attributes('-topmost', True)
        self.update()
        self.attributes('-topmost', False)
