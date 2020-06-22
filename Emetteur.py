class Emetteur:
    def __init__(self, name, pos, power, decay):
        self.name = name
        self.power = power
        self.decay = decay
        self.pos = pos
        self.distance = int(abs(power) / abs(decay))

