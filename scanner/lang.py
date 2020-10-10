class Edge:
    def __init__(self):
        self.__include_ranges = []
        self.__exclude_ranges = []

    def include(self, start, end=None):
        if not end: end=start
        self.__include_ranges.append((start, end))
        return self

    def exclude(self, start, end=None):
        if not end: end=start
        self.__exclude_ranges.append((start, end))
        return self

    def contains_in_includes(self,char):
        for start, end in self.__include_ranges:
            if start<= char <= end:
                return True
        return False

    def contains_in_excludes(self,char):
        for start, end in self.__exclude_ranges:
            if start <= char <= end:
                return False
        return True

    def __contains__(self, char):
        if len(self.__exclude_ranges)==0:
            return self.contains_in_includes(char)
        elif len(self.__include_ranges)==0:
            return self.contains_in_excludes(char)
        else:
            return self.contains_in_includes(char) or self.contains_in_excludes(char)
class DFANode:
    def __init__(self, action=None):
        self.action = action
        self.children = []

    def append(self, edge, child):
        self.children.append((edge, child))
        return self

    def match(self, char):
        for edge, child in self.children:
            if char in edge:
                return child
        return self.action


class FinalStateNode(DFANode):
    def __init__(self, action, push_back_mode):
        super().__init__(action)
        self.push_back_mode = push_back_mode

    def should_push_back(self):
        return self.push_back_mode


