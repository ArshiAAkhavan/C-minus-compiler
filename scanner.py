from error import *


class Edge:
    def __init__(self):
        self.include_ranges = []
        self.exclude_ranges = []

    def include(self, start, end):
        self.include_ranges.append((start, end))
        return self

    def exclude(self, start, end):
        self.exclude_ranges.append((start, end))
        return self

    def __contains__(self, char):
        for start, end in self.exclude_ranges:
            if start <= char and char <= end:
                return False

        for start, end in self.include_ranges:
            if char < start or end < char:
                return False
        return True


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
    def __init__(self, root, input_provider):
        self.root = root
        self.input_provider = input_provider

    def can_generate_token(self):
        return self.input_provider.has_next()

    def get_next_token(self):
        state = self.root
        lexeme = ""
        while(True):

            if isinstance(state, FinalStateNode):
                if state.should_push_back():
                    self.input_provider.push_back(lexeme[-1])
                    lexeme = lexeme[:-1]
                return state.action(lexeme)
            elif not isinstance(state, DFANode):
                return state(lexeme)

            if not self.input_provider.has_next():
                break
            lexeme += self.input_provider.get_next_char()
            state = state.match(lexeme[-1])


def main():
    from buffer_reader import BufferReader

    # implementing number regex
    number_regex = DFANode(lambda lexeme: print(
        TokenMissMatchException(lexeme)))
    middle_state = DFANode(lambda lexeme: print(
        TokenMissMatchException(lexeme)))
    final_state = FinalStateNode(
        lambda lexeme: print(f"lexeme is {lexeme}"), True)
    middle_state.append(Edge().include("0", "9"), middle_state).append(
        Edge().exclude("0", "9"), final_state)
    number_regex.append(Edge().include("0", "9"), middle_state)

    sc = Scanner(number_regex, BufferReader("input.txt", 30))

    while(sc.can_generate_token()):
        try:
            sc.get_next_token()
        except TokenMissMatchException as e:
            print(e)
        except NotEnoughCharacterException as e:
            print(e)
            break


if __name__ == "__main__":
    main()
