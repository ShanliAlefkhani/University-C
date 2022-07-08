class Node:
    def __init__(self, name, children=None, parent=None):
        self.name = name
        self.children = children
        self.parent = parent

    def __str__(self):
        return self.name

    def print(self, level=-1):
        s = ""
        if self.parent:
            s = level * "\t" + str(self) + "\n"
        for c in self.children:
            s += c.print(level + 1)

        return s
