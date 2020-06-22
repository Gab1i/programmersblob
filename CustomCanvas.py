import os
from tkinter import Canvas, PhotoImage, NW


class CustomCanvas(Canvas):
    """
    Class that creates a button with an image
    """

    def __init__(self, parent, width, height, bg):
        """
        Constructor:
        """
        if os.path.isfile(bg):
            self._file = bg
            self._image = PhotoImage(file=bg)
            Canvas.__init__(self, parent, width=width, height=height, highlightthickness=0, relief='ridge')
            self.create_image(0, 0, anchor=NW, image=self._image)
        else:
            Canvas.__init__(self, parent, width=width, height=height, highlightthickness=0, relief='ridge', bg=bg)

        self.Clickables = []

        self.bind('<Button-1>', self._onClick)
        self.bind('<Motion>', self._onMotion)

    def _onClick(self, evt):
        for btn in self.Clickables:
            if evt.x in range(btn.x[0], btn.x[1]) and evt.y in range(btn.y[0], btn.y[1]):
                btn.OnClick()

    def _onMotion(self, evt):
        for btn in self.Clickables:
            if evt.x in range(btn.x[0], btn.x[1]) and evt.y in range(btn.y[0], btn.y[1]):
                btn.Toggle()
