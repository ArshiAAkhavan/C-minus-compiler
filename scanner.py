from errors import *
import actions

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
                return state.action(self.input_provider.get_line_no(),lexeme)
            elif not isinstance(state, DFANode):
                return state(self.input_provider.get_line_no(),lexeme)

            if not self.input_provider.has_next():
                break
            lexeme += self.input_provider.get_next_char()
            state = state.match(lexeme[-1])


def main():
    from buffer_reader import BufferReader

    start = DFANode(actions.error_gen)
    # implementing number regex
    num_middle_state = DFANode(actions.error_gen)
    num_final_state = FinalStateNode(actions.num_token_gen, True)
    num_middle_state.append(Edge().include("0", "9"), num_middle_state).append(Edge().exclude("0", "9"), num_final_state)\
        .append(Edge().exclude("a", "z"), num_final_state).append(Edge().exclude("A", "Z"), num_final_state)
    start.append(Edge().include("0", "9"), num_middle_state)
    # implementing id/keyword
    id_middle_state = DFANode(actions.error_gen)
    id_final_state = FinalStateNode(actions.id_token_gen, True)
    id_middle_state.append(Edge().include("0", "9"), id_middle_state).append(Edge().include("a", "z"), id_middle_state)\
        .append(Edge().include("A", "Z"), id_middle_state).append(Edge().exclude("0", "9"), id_final_state)\
        .append(Edge().exclude("a", "z"), id_final_state).append(Edge().exclude("A", "Z"), id_final_state)
    start.append(Edge().include("a", "z"), id_middle_state).append(Edge().include("A", "Z"), id_middle_state)


    sc = Scanner(start, BufferReader("input.txt", 30))

    while(sc.can_generate_token()):
        try:
            sc.get_next_token()
        except TokenMissMatchException as e:
            print(e)
        except NotEnoughCharacterException as e:
            print(e)
            break
    import tables

    print(tables.get_token_table())
    tables.get_error_table().end()


if __name__ == "__main__":
    main()
