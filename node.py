class Node:
    def __init__(self, name, children=None, parent=None):
        self.name = name
        self.children = children
        self.parent = parent

    def __str__(self):
        return self.name

    def print(self):
        return
