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


class Other_edge(Edge):
    pass


class DFA_node:
    def __init__(self, action=None):
        self.action = action
        self.children = []

    def append(self, edge, child):
        self.children.append((edge, child))
        return self

    def match(self, char):
        for edge, child in self.children:
            if char in edge:
                return edge, child
        return None


class Final_state_node(DFA_node):
    pass


class Scanner:
    def __init__(self, root, input_provider):
        self.root = root
        self.input_provider = input_provider

    def get_next_token(self):
        current_state = self.root
        current_edge = None
        current_lexeme = ""
        current_char = ''
        while(self.input_provider.has_next()):
            if isinstance(current_edge, Other_edge):
                self.input_provider.push_back(current_char)
                current_lexeme = current_lexeme[:-1]

            if isinstance(current_state, Final_state_node):
                return current_state.action(current_lexeme)
            
            current_char=self.input_provider.get_next_char()
            current_lexeme+=current_char
            try:                                                                
                # returns an standard edge,state
                current_edge,current_state=current_state.match(current_char)
            except TypeError:                                                   
                # returns None
                try:
                    # is a final state
                    return current_state.action(current_lexeme)
                except TypeError:
                    # is not a final state
                    raise TokenMissMatchException(current_lexeme)


def main():
    from buffer_reader import Buffer_reader

    # implementing number regex
    number_regex = DFA_node()
    middle_state = DFA_node()
    final_state = Final_state_node(lambda lexeme: print(f"lexeme is {lexeme}"))
    middle_state.append(Edge().include("0", "9"), middle_state).append(
        Other_edge().exclude("0", "9"), final_state)
    number_regex.append(Edge().include("0", "9"), middle_state)

    sc = Scanner(number_regex, Buffer_reader("input.txt", 30))

    while(True):
        try:
            sc.get_next_token()
        except TokenMissMatchException as e:
            print(e)


if __name__ == "__main__":
    main()
