from anytree import Node, RenderTree
from parser.grammer import Terminal
from scanner.tokens import TokenType


class LL1:
    def __init__(self, token_generator, grammer):
        self.token_generator = token_generator
        self.grammer = grammer
        self.p_table = {}
        self.create_parse_table()

    def create_parse_table(self):
        for rule in self.grammer.rules:
            for predict in rule.predict_set:
                self.p_table[(rule.left.name, predict.name)] = [p.name for p in rule.right]
        for nt in self.grammer.non_terminals:
            for item in nt.follow:
                if (nt, item) not in self.p_table:
                    self.p_table[(nt.name, item)] = "synch"

    def generate_parse_tree(self):
        root=Node(self.grammer.rules[0].left.name)
        stack = [root]
        while len(stack) and self.token_generator.can_generate_token():
            token = self.token_generator.get_next_token()
            if token.type == TokenType.COMMENT or token.type == TokenType.WHITE_SPACE: continue
            # todo @ghazal baraye grammer unit ye Sm e behtar peyda kon
            grammer_node = stack.pop()
            ### terminal
            if isinstance(self.grammer.get_element_by_id(grammer_node.name), Terminal):
                ### not matching
                if grammer_node.name != token.lexeme:
                    raise Exception(f"expected {grammer_node.name}!")
            ### none_terminal
            else:
                ### matching
                if (grammer_node.name, token.lexeme) in self.p_table and self.p_table[(grammer_node.name, token.lexeme)] != "synch":

                    new_units = [Node(g,parent=grammer_node) for g in self.p_table[(grammer_node.name, token.lexeme)]]
                    stack.extend([n for n in new_units][::-1])
                ### panicing
                else:
                    ### synch
                    while (grammer_node.name, token.lexeme) not in self.p_table:
                        token = self.token_generator.get_next_token()
