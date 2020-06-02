from Emetteur import Emetteur
from Capteur import Capteur

class Agent(object):
    def __init__(self, name, line, col):
        self.coord = (line, col)
        self.name = name
        self.emetteurs = {}
        self.capteurs = {}


class Veine(Agent):
    max = 10
    count = 0

    def __init__(self, line, col):
        super().__init__("veine", line, col)
        self.capteurs['food'] = Capteur('food')
        Veine.count += 1


class Food(Agent):
    def __init__(self, name, line, col):
        super().__init__(name, line, col)
        self.emetteurs['food'] = Emetteur('food', 20, 1)

