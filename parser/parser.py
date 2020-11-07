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
        self.root = Node(self.grammer.rules[0].left.name)

    def create_parse_table(self):
        for rule in self.grammer.rules:
            for predict in rule.predict_set:
                self.p_table[(rule.left.name, predict.name)] = [p.name for p in rule.right]

        for nt in self.grammer.non_terminals:
            # if nt.name =="Declaration-list":
            #     print()
            for item in nt.follow:
                if self.grammer.get_element_by_id("ε") not in nt.first and (nt, item) not in self.p_table:
                    self.p_table[(nt.name, item.name)] = "synch"

    def generate_parse_tree(self):
        self.stack = [self.root]
        token = self.get_next_valid_token()

        while len(self.stack):
            # todo @ghazal baraye grammer node ye Sm e behtar peyda kon
            grammer_node = self.get_next_valid_grammer_node()
            ### terminal
            if isinstance(self.grammer.get_element_by_id(grammer_node.name), Terminal):
                ### not matching
                if grammer_node.name != self.get_token_matcher(token):
                    # todo should be changed to something else i thing
                    # raise Exception(f"expected {grammer_node.name}!")
                    print(f"expected {grammer_node.name}!")
                if len(self.stack): token = self.get_next_valid_token()
            ### none_terminal
            else:
                key = (grammer_node.name, self.get_token_matcher(token))
                if key in self.p_table and self.p_table[key] != "synch":
                    self.update_stack(grammer_node, key)
                else:
                    token = self.panic(grammer_node, key, token)
        return self.root

    def update_stack(self, grammer_node, key):
        ### should handle epsilon for ε and (ID,lexeme) & (KEYWORD,lexeme) for id,keyword here
        self.stack.extend([Node(g, parent=grammer_node) for g in self.p_table[key]][::-1])

    def panic(self, grammer_node, key, token):
        while key not in self.p_table:
            token = self.get_next_valid_token()
            key = (grammer_node.name, self.get_token_matcher(token))
        return token

    def get_next_valid_token(self):
        token = self.token_generator.get_next_token()
        while token.type == TokenType.COMMENT or (
                token.type == TokenType.WHITE_SPACE and token.lexeme != chr(26)):  # EOF
            token = self.token_generator.get_next_token()
        return token

    def get_next_valid_grammer_node(self):
        grammer_node = self.stack.pop()
        while grammer_node.name == "ε":
            grammer_node = self.stack.pop()
        return grammer_node

    # todo @ghazal in gharare age token NUM ya ID bud, NUM o ID bargardune , dar gheyr e in surat lexeme ro
    @staticmethod
    def get_token_matcher(token):
        return (token.lexeme, token.type.name)[token.type in [TokenType.NUM, TokenType.ID]]

    def export_parse_tree(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            for pre, fill, node in RenderTree(self.root):
                f.write("%s%s\n" % (pre, node.name))
