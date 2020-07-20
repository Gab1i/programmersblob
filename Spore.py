from random import randint


class Spore:
    def __init__(self, sexe, case):
        self._sexe = sexe
        self._case = case

    def Move(self, neighbors):
        neighbors = list(neighbors)
        r = randint(0, len(neighbors)-1)

        case = neighbors[r]
        case.AddSpore(self)
        self._case.RemoveSpore(self)
        self._case = case

        if len(self._case.TimeToKen()) == 2:
            #self._case.Spores = []
            return True

        return False

