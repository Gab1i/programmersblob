from tkinter import *
from CustomButton import CustomButton
from CustomCanvas import CustomCanvas


class Menu(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Der Blob')
        self.width, self.height = 600, 400

        self.positionX = int(self.winfo_screenwidth() / 2 - self.width / 2)
        self.positionY= int(self.winfo_screenheight() / 2 - self.height / 2)

        self.geometry("+{}+{}".format(self.positionX, self.positionY))

        self.leftCanvas = CustomCanvas(self, width=self.width, height=self.height, bg='UI/bg_menu.png')
        self.leftCanvas.pack(side=LEFT)

        self.cancel = CustomButton(self.leftCanvas, 'UI/cancel.png', self.width-20, 20,
                                   'UI/cancel_hover.png', self.closeApp)

        self.start = CustomButton(self.leftCanvas, 'UI/btn_start.png', self.width-70, self.height-35, '',
                                  self.startSimulation)

        self.wm_overrideredirect(True)
        self.update_idletasks()
        self.lift()
        self.attributes('-topmost', True)
        self.update()
        self.attributes('-topmost', False)

        self.bind('<Motion>', self._onMotion)

    def closeApp(self):
        print('CLOSE')
        self.quit()

    def startSimulation(self):
        print("START")

    def _onMotion(self, evt):
        """self.positionX = , self.positionY
        if evt.state == 'Button1':
            self.geometry("+{}+{}".format(self.positionX, self.positionY))

        #print(evt)
        #if evt.x > 200: self.rightCanvas.focus_force()
        #else: self.leftCanvas.focus_force()"""
        pass
