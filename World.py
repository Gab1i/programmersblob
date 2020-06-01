from Case import Case
# ON ECRIT LINE, COL (===== Y, X)
class World:
    def __init__(self, size):
        self.size = size
        self.grid = [Case() for i in range(size * size)]
        self.agents = []

    def pos2coord(self, pos):
        line = pos // self.size
        col = pos % self.size
        return (line, col)

    def coord2pos(self, line, col):
        return int(line * self.size + col)

    def setField(self):
        for agent in self.agents:
            for key, e in agent.emetteurs.items():
                d = e.power / e.decay

                for i in range(int(d)):
                    (line, col) = agent.coord
                    neighbors = self.neighbor(line, col, i)
                    for n in neighbors:
                        self.grid[n].updateField(e.name, e.power - e.decay * i)

    def neighbor(self, line, col, n):
        # TODO : Attention aux extrêmités
        l = []
        for y in range(int(col - n), int(col + n + 1)):
            l.append(self.coord2pos(line - n, y))
            l.append(self.coord2pos(line + n, y))

        for x in range(int(line - n + 1), int(line + n)):
            l.append(self.coord2pos(x, col + n))
            l.append(self.coord2pos(x, col - n))

        return set(l)

    def birthControl(self):
        pass

    def sarahConnor(self):
        pass

    def tick(self):
        self.setField()
        self.sarahConnor()
        self.birthControl()

    def run(self, loop):
        for i in range(loop):
            self.tick()

