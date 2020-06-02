class Case:
    maxFields = {}

    def __init__(self):
        self.fields = {}
        self.agent = None

    def updateField(self, name, value):
        if name in self.fields:
            self.fields[name] += value
        else:
            self.fields[name] = value

        if name in Case.maxFields:
            if self.fields[name] > Case.maxFields[name][1]: Case.maxFields[name][1] = self.fields[name]

            if self.fields[name] < Case.maxFields[name][0]: Case.maxFields[name][0] = self.fields[name]
        else:
            Case.maxFields[name] = [value, value]

    def isAgent(self):
        return self.agent

    def __repr__(self):
        return str(self.fields)
