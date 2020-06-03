from Emetteur import Emetteur
from Capteur import Capteur

class Agent(object):
    def __init__(self, name, line, col):
        self.coord = (line, col)
        self.name = name
        self.emetteurs = {}
        self.capteurs = {}


class Veine(Agent):
    max = 3
    count = 0

    def __init__(self, line, col):
        super().__init__("veine", line, col)
        self.capteurs['food'] = Capteur('food')
        Veine.count += 1

    def feed(self, food):
        print("feed")
        qte = food.suckFood(5)
        Veine.max += qte


class Food(Agent):
    def __init__(self, name, line, col, nutriments, qte):
        super().__init__(name, line, col)
        self.emetteurs['food'] = Emetteur('food', 20, 1)

        self.nutriments = {}
        self.qte = qte

    def suckFood(self, howMuch):
        q = max(0, self.qte - howMuch)
        p = max(0, howMuch - self.qte)
        self.qte = q
        print("Food : {0}".format(self.qte))
        return p
