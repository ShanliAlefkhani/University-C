class Node:
    def __init__(self, name, children=None, parent=None):
        self.name = name
        self.children = children
        self.parent = parent

    def __str__(self):
        return self.name

    def tree_print(self, level=0):
        print(level * "\t", str(self))
        for c in self.children:
            c.tree_print(level + 1)
