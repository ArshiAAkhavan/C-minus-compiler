from parser.tree import PTNode


class LL1:
    def __init__(self, token_generator, grammer):
        self.token_generator = token_generator
        self.grammer = grammer
        self.p_table = {}
        self.create_parse_table()

    def create_parse_table(self):
        for rule in self.grammer.rules:
            for predict in rule.predict_set:
                self.p_table[(rule.left, predict)] = rule.right
        for nt in self.grammar.non_terminals:
            for item in nt.follow:
                if (nt, item) not in self.p_table:
                    self.p_table[(nt, item)] = "synch"

    def generate_parse_tree(self):
        stack = [PTNode("$"), PTNode(self.grammer.rules[0].left)]
        while len(stack) and self.token_generator.can_generate_token():
            token = self.token_generator.get_next_token()
            # todo @ghazal baraye grammer unit ye Sm e behtar peyda kon
            grammer_unit = stack.pop()
            productions=self.p_table[(grammer_unit,token.vlaue.lexeme)]