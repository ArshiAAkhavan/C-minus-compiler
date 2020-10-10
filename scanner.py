from errors import *
import actions

class Edge:
    def __init__(self):
        self.include_ranges = []
        self.exclude_ranges = []

    def include(self, start, end=None):
        if not end: end=start
        self.include_ranges.append((start, end))
        return self

    def exclude(self, start, end=None):
        if not end: end=start
        self.exclude_ranges.append((start, end))
        return self

    def contains_in_includes(self,char):
        for start, end in self.include_ranges:
            if start<= char <= end:
                return True
        return False

    def contains_in_excludes(self,char):
        for start, end in self.exclude_ranges:
            if start <= char <= end:
                return False
        return True

    def __contains__(self, char):
        if len(self.exclude_ranges)==0:
            return self.contains_in_includes(char)
        elif len(self.include_ranges)==0:
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


class Scanner:
    def __init__(self, root, input_provider,language):
        self.root = root
        self.input_provider = input_provider
        self.language=language

    def can_generate_token(self):
        return self.input_provider.has_next()

    def get_next_token(self):
        state = self.root
        lexeme = ""
        line_no=self.input_provider.get_line_no()
        while(True):
            if isinstance(state, FinalStateNode):
                if state.should_push_back():
                    self.input_provider.push_back(lexeme[-1])
                    lexeme = lexeme[:-1]
                return state.action(line_no,lexeme)
            elif not isinstance(state, DFANode):
                return state(line_no,lexeme)

            if not self.input_provider.has_next():
                break
            lexeme += self.input_provider.get_next_char()
            if lexeme[-1] not in self.language:
                return state.action(line_no,lexeme)
            state = state.match(lexeme[-1])


def main():
    pass
if __name__ == "__main__":
    main()
