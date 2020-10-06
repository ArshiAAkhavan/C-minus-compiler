class TokenMissMatchException(Exception):
    def __init__(self, token_lexeme):
        super(TokenMissMatchException, self).__init__(
            f"could not match lexeme[{token_lexeme}] with any known regular expressions...")


class Edge:
    def __init__(self):
        self.include_ranges = []
        self.exclude_ranges = []

    def include(self, start, end):
        self.include_ranges.append((start, end))

    def exclude(self, start, end):
        self.exclude_ranges.append((start, end))

    def __contains__(self,char):
        for r in self.exclude_ranges:
            if r[0]<=char and char<=r[1]:
                return False
        
        for r in self.include_ranges:
            if char<r[0] or r[1]<char:
                return False
        return True

class Node:
    def __init__(self, action=None):
        self.action = action
        self.children = []
        self.current_token = ""

    def append(self, edge, child):
        self.children.append((edge, child))

    def match(self, char):
        for (edge, child), _ in self.children:
            if char in edge:
                return child
        try:
            return self.action(self.current_token)
        except TypeError:
            raise TokenMissMatchException


class DFA:
    pass
