from tkinter import Canvas, PhotoImage


class Button(Canvas):
    """
    Class that creates a button with an image
    """

    def __init__(self, image, image_hover='', on_click=None):
        """
        Constructor:
        image: path of the image
        image_hover: path of the image to show on mouse hover
        on_click: call back for on click function
        """
        self._image_hover = image_hover
        self._image_normal = image
        self._image = PhotoImage(file=image)

        Canvas.__init__(self, width=self._image.width()+1, height=self._image.height()+2, highlightthickness=0, bg='#5c5c5c')

        self._button = self.create_image(self._image.height()/2, self._image.width()/2, image=self._image)

        self._state = False

        self.bind('<Button-1>', on_click)
        self.bind('<Enter>', self._onHover)
        self.bind('<Leave>', self._onHover)

    def _onHover(self, evt):
        self._state = not self._state
        self._hover(self._state)

    def _hover(self, state):
        """
        Method to trigger when the mouse is in the button
        """
        if self._image_hover != '':
            if state:
                self._image.configure(file=self._image_hover)
            else:
                self._image.configure(file=self._image_normal)
