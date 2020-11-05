from anytree import NodeMixin, RenderTree


class PTNode(NodeMixin):
    def __init__(self, terminal, parent=None, children=None):
        self.name = terminal.name
        self.children = children
        self.parent = parent
