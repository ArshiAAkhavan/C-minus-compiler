from anytree import Node, RenderTree
from parser.grammer import Terminal
from scanner.tokens import TokenType


class LL1:
    def __init__(self, token_generator, grammer):
        self.token_generator = token_generator
        self.grammer = grammer
        self.p_table = {}
        self.stack = []
        self.create_parse_table()

    def create_parse_table(self):
        for rule in self.grammer.rules:
            for predict in rule.predict_set:
                self.p_table[(rule.left.name, predict.name)] = [p.name for p in rule.right]
        for nt in self.grammer.non_terminals:
            for item in nt.follow:
                if (nt, item) not in self.p_table:
                    self.p_table[(nt.name, item)] = "synch"

    def get_next_valid_token(self):
        token = self.token_generator.get_next_token()
        while token.type == TokenType.COMMENT or token.type == TokenType.WHITE_SPACE:
            token = self.token_generator.get_next_token()
        return token

    def get_next_valid_grammer_node(self):
        grammer_node = self.stack.pop()
        while grammer_node.name == "ε":
            grammer_node = self.stack.pop()
        return grammer_node

    def generate_parse_tree(self):
        root = Node(self.grammer.rules[0].left.name)
        self.stack = [root]
        token = self.get_next_valid_token()
        while len(self.stack) and self.token_generator.can_generate_token():
            # todo @ghazal baraye grammer node ye Sm e behtar peyda kon
            grammer_node = self.get_next_valid_grammer_node()
            ### terminal
            if isinstance(self.grammer.get_element_by_id(grammer_node.name), Terminal):
                ### not matching
                if grammer_node.name != (token.lexeme, token.type.name)[token.type in [TokenType.NUM, TokenType.ID]]:
                    raise Exception(f"expected {grammer_node.name}!")
                token = self.get_next_valid_token()
            ### none_terminal
            else:
                ### matching
                key = (grammer_node.name, (token.lexeme, token.type.name)[token.type in [TokenType.NUM, TokenType.ID]])
                if key in self.p_table and self.p_table[key] != "synch":
                    new_units = [Node(g, parent=grammer_node) for g in self.p_table[key]]
                    self.stack.extend([n for n in new_units][::-1])
                ### panicing
                else:
                    ### synch
                    while key not in self.p_table:
                        token = self.get_next_valid_token()
                        key = (
                            grammer_node.name,
                            (token.lexeme, token.type.name)[token.type in [TokenType.NUM, TokenType.ID]])
