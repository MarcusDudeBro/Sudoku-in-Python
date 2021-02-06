class Tree:
    class Node:
        def __init__(self, element, parent=None):
            self.element = element
            self.parent = parent
            self.children = None

        def get_element(self):
            return self.element

    def __init__(self):
        self.size = 0
        self.root = None

    def get_root(self):
        return self.root

    def is_root(self, node):
        if node == self.root:
            return True
        return False

    def parent(self, node):
        return node.parent

    def num_children(self, node):
        return len(node.children)

    def is_leaf(self, node):
        if len(node.children) == 0:
            return True
        return False

    def children(self, node):
        return node.children

    def remove(self, node):
        node.parent.children.remove(node)

    def __len__(self):
        return self.size

    def is_empty(self):
        if self.size == 0:
            return True
        return False

    def add_children(self, parent, children):
        for i in range(len(children)):
            children[i] = self.Node(children[i], parent)
        parent.children = children
        return children

    def add_root(self, element):
        self.root = self.Node(element)
        return self.root
