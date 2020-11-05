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

    def generate_parse_tree(self):
        stack = [self.grammer.rules[0].left, "$"]

        while len(stack) and self.token_generator.can_generate_token():
            pass
