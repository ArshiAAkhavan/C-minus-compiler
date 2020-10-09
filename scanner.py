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
    def __init__(self, root, input_provider):
        self.root = root
        self.input_provider = input_provider

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
            state = state.match(lexeme[-1])


def main():
    from buffer_reader import BufferReader

    start = DFANode(actions.error_gen)
    # implementing number regex
    # num_middle_state = DFANode(actions.error_gen)
    # num_final_state = FinalStateNode(actions.num_token_gen, True)
    # num_middle_state.append(Edge().include("0", "9"), num_middle_state).append(Edge().exclude("0", "9").exclude("a","z").exclude("A","Z"), num_final_state)
    # start.append(Edge().include("0", "9"), num_middle_state)

    # implementing id/keyword
    id_middle_state = DFANode(actions.error_gen)
    id_final_state = FinalStateNode(actions.id_token_gen, True)
    id_middle_state.append(Edge().include("0", "9").include("a", "z").include("A", "Z"), id_middle_state)\
        .append(Edge().exclude("0", "9").exclude("a", "z").exclude("A", "Z"), id_final_state)
    start.append(Edge().include("a", "z").include("A", "Z"), id_middle_state)
    # # implementing symbols
    # symbols_group_final_state = FinalStateNode(actions.symbol_token_gen, False) # 5
    # equals_final_state = FinalStateNode(actions.symbol_token_gen, False) # 7
    # assign_middle_state = DFANode(actions.error_gen) # 6
    # star_middle_state = DFANode(actions.error_gen) # 8
    # assign_star_final_state = FinalStateNode(actions.symbol_token_gen, True) # 9
    # start.append(Edge().include(":", "<").include(",", ",").include("(", ")").include("[", "[").include("]", "]")
    #              .include("{", "{").include("}", "}").include("+", "+").include("-", "-"), symbols_group_final_state)
    # start.append(Edge().include("=", "="), assign_middle_state)
    # start.append(Edge().include("*", "*"), star_middle_state)
    # assign_middle_state.append(Edge().include("=", "="), equals_final_state).append(Edge().exclude("=", "="), assign_star_final_state)
    # star_middle_state.append(Edge().exclude("/", "/"), assign_star_final_state)

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
    tables.get_symbol_table().end()


if __name__ == "__main__":
    main()
