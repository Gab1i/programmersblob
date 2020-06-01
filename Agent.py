from Emetteur import Emetteur


class Agent(object):
    def __init__(self, name, line, col):
        self.coord = (line, col)
        self.name = name
        self.emetteurs = {}


class Veine(Agent):
    def __init__(self):
        pass


class Food(Agent):
    def __init__(self, name, line, col):
        super().__init__(name, line, col)
        self.emetteurs['food'] = Emetteur('food', 20, 1)