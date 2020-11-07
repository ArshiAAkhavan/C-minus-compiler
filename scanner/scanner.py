from scanner.lang import DFANode, FinalStateNode


class Scanner:
    def __init__(self, root, input_provider, language):
        self.root = root
        self.input_provider = input_provider
        self.language = language

    def get_line_no(self):
        return self.input_provider.get_line_no()

    def can_generate_token(self):
        return self.input_provider.has_next()

    def get_next_token(self):
        state = self.root
        lexeme = ""
        line_no = self.get_line_no()
        while True:
            if isinstance(state, FinalStateNode):
                if state.should_push_back():
                    self.input_provider.push_back(lexeme[-1])
                    lexeme = lexeme[:-1]
                return state.action(line_no, lexeme)
            elif not isinstance(state, DFANode):
                return state(line_no, lexeme)

            if not self.input_provider.has_next():
                break

            lexeme += self.input_provider.get_next_char()
            if lexeme[-1] not in self.language and not state.is_universal():
                return state.action(line_no, lexeme)
            state = state.match(lexeme[-1])
