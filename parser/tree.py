from anytree import NodeMixin, RenderTree


class PTNode(NodeMixin):
    def __init__(self, terminal, parent=None, children=None):
        self.terminal = terminal
        try:
            self.name = terminal.name
        except Exception as e:
            pass
            self.children = children
        self.parent = parent
