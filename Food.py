from Emetteur import Emetteur


class Food(Emetteur):
    def __init__(self, name, pos, power, decay, qte):
        super().__init__(name, pos, power, decay)
        self.quantity = qte
        self.status = True

    def Eat(self, howMuch):
        q = max(0, self.quantity - howMuch)
        p = max(0, howMuch - self.quantity)
        self.quantity = q

        print("Je me fais manger")
        if self.quantity <= 0: self.status = False
        return p


