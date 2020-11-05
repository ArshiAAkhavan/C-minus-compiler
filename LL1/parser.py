class LL1:
    def __init__(self, token_generator, grammar):
        self.token_generator = token_generator
        self.grammar = grammar
        self.p_table = {}
        self.create_parse_table()

    def create_parse_table(self):
        for rule in self.grammar.rules:
            for predict in rule.predict_set:
                self.p_table[(rule.left, predict)] = rule.right
        for nt in self.grammar.non_terminals:
            for item in nt.follow:
                if (nt, item) not in self.p_table:
                    self.p_table[(nt, item)] = "synch"

    def generate_parse_tree(self):
        stack = [self.grammar.rules[0].left, "$"]

        while len(stack) and self.token_generator.can_generate_token():
            pass
