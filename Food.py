from Emetteur import Emetteur


class Food(Emetteur):
    """
    ratio = Proteine/Glucide
    concentration = <= 1
    """
    def __init__(self, name, pos, decay, qte, concentration, ratio):
        diff = abs(2 - ratio)
        if diff == 0: res = 9999999 * concentration
        else: res = (1 / diff) * (concentration)

        super().__init__(name, pos, res, decay)
        self.quantity = qte
        self.status = True

        self.concentration = concentration
        self.ratio = ratio
        self.quantity = qte

    def Eat(self, howMuch):
        q = max(0, self.quantity - howMuch)
        p = max(0, howMuch - self.quantity)
        self.quantity = q

        if self.quantity <= 0: self.status = False
        return p

    def Eat(self):
        self.quantity -= 1
        if self.quantity <= 0: self.status = False
        return {
            "proteine": self.ratio,
            "glucide": 1 - self.ratio,
        }
