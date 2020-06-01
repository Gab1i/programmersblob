class Case:
    def __init__(self):
        self.fields = {}
        self.agent = False

    def updateField(self, name, value):
        if name in self.fields:
            self.fields[name] += value
        else:
            self.fields[name] = value

    def isAgent(self):
        return self.agent