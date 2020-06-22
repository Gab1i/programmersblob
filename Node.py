class Node:
    Count = 0
    Seen = []

    def __init__(self, case, parent):
        self.case = case
        self.parent = parent

        self.seen = False