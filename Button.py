from tkinter import Canvas, PhotoImage


class Button(Canvas):
    """
    Class that creates a button with an image
    """

    def __init__(self, canvas, image, x, y, image_hover=''):
        """
        Constructor:
        canvas : canvas where the button is
        file : file of the image
        image : PhotoImage of the image
        button : image in the canvas
        coord_x : range coordinate in the horizontal axis
        coord_y : range coordinate in the vertical axis
        """
        self._canvas = canvas
        self._image_hover = image_hover
        self._image_normal = image
        self._image = PhotoImage(file=image)
        self._button = canvas.create_image(x, y, image=self._image)
        self._coord_x = [int(canvas.coords(self._button)[0] - self._image.width() / 2),
                         int(canvas.coords(self._button)[0] + self._image.width() / 2)]
        self._coord_y = [int(canvas.coords(self._button)[1] - self._image.height() / 2),
                         int(canvas.coords(self._button)[1] + self._image.height() / 2)]
        self._state = False

    def _get_coord_x(self):
        """Getter of coord_x"""
        return self._coord_x

    def _get_coord_y(self):
        """Getter of coord_y"""
        return self._coord_y

    x = property(_get_coord_x)
    y = property(_get_coord_y)

    def hover(self, state):
        """
        Method to trigger when the mouse is in the button
        """
        if self._image_hover != '':
            if state:
                self._image.configure(file=self._image_hover)
            else:
                self._image.configure(file=self._image_normal)

    def toggle(self):
        self._state = not self._state
        self.hover(self._state)