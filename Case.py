class Case:
    maxFields = {}

    def __init__(self):
        self.fields = {}
        self.agent = False

    def updateField(self, name, value):
        if name in self.fields:
            self.fields[name] += value
        else:
            self.fields[name] = value

        if name in Case.maxFields:
            if value > Case.maxFields[name][1]: Case.maxFields[name][1] = value
            if value < Case.maxFields[name][0]: Case.maxFields[name][0] = value
        else:
            Case.maxFields[name] = [value, value]

    def isAgent(self):
        return self.agent