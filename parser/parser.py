from anytree import Node, RenderTree, PreOrderIter
from parser.grammar import Terminal
from scanner.tokens import TokenType


class NoTokenLeftException(Exception):
    pass


class LL1:
    def __init__(self, token_generator, grammar):
        self.token_generator = token_generator
        self.grammar = grammar
        self.p_table = {}
        self.stack = []
        self.errors = []
        self.create_parse_table()
        self.root = Node(self.grammar.rules[0].left.name)

    def create_parse_table(self):
        for rule in self.grammar.rules:
            for predict in rule.predict_set:
                self.p_table[(rule.left.name, predict.name)] = [p.name for p in rule.right]

        for nt in self.grammar.non_terminals:
            for item in nt.follow:
                if (nt.name, item.name) not in self.p_table:
                    self.p_table[(nt.name, item.name)] = "synch"

    def generate_parse_tree(self):
        self.stack = [self.root]
        token = self.get_next_valid_token()
        grammar_node= None
        try:
            while len(self.stack):
                # todo @ghazal baraye grammar node ye Sm e behtar peyda kon
                grammar_node = self.get_next_valid_grammar_node()
                grammar_node.token = token
                ### terminal
                if isinstance(self.grammar.get_element_by_id(grammar_node.name), Terminal):
                    ### not matching
                    if grammar_node.name != self.get_token_matcher(token):
                        self.errors.append((self.token_generator.get_line_no(), f"Missing {grammar_node.name}"))
                    if len(self.stack): token = self.get_next_valid_token()
                ### none_terminal
                else:
                    key = (grammar_node.name, self.get_token_matcher(token))
                    if key in self.p_table and self.p_table[key] != "synch":
                        self.update_stack(grammar_node, key)
                    else:
                        token = self.panic(grammar_node, key, token)
        except NoTokenLeftException:
            self.remove_node(grammar_node)
            [self.remove_node(g) for g in self.stack]

        return self.root

    def update_stack(self, grammar_node, key):
        ### should handle epsilon for ε and (ID,lexeme) & (KEYWORD,lexeme) for id,keyword here
        self.stack.extend([Node(g, parent=grammar_node) for g in self.p_table[key]][::-1])

    def panic(self, grammar_node, key, token):
        while key not in self.p_table:
            self.errors.append((self.token_generator.get_line_no(), f"illegal {token.lexeme}"))
            token = self.get_next_valid_token()
            key = (grammar_node.name, self.get_token_matcher(token))
        if self.p_table[key] != 'synch':
            self.update_stack(grammar_node, key)
            return token

        self.errors.append((self.token_generator.get_line_no(), f"Missing {grammar_node.name}"))
        self.remove_node(grammar_node)
        return token

    @staticmethod
    def remove_node(grammar_node):
        children = list(grammar_node.parent.children)
        children.remove(grammar_node)
        grammar_node.parent.children = tuple(children)

    def get_next_valid_token(self):
        try:
            token = self.token_generator.get_next_token()
            while token.type == TokenType.COMMENT or (
                    token.type == TokenType.WHITE_SPACE and token.lexeme != chr(26)):  # EOF
                token = self.token_generator.get_next_token()
            return token
        except:
            raise NoTokenLeftException()

    def get_next_valid_grammar_node(self):
        grammar_node = self.stack.pop()
        while grammar_node.name == "ε":
            grammar_node = self.stack.pop()
        return grammar_node

    # todo @ghazal in gharare age token NUM ya ID bud, NUM o ID bargardune , dar gheyr e in surat lexeme ro
    @staticmethod
    def get_token_matcher(token):
        return (token.lexeme, token.type.name)[token.type in [TokenType.NUM, TokenType.ID]]

    def export_parse_tree(self, path):
        for node in PreOrderIter(self.root):
            if node.name == "ε":
                node.name = "epsilon"
            elif node.name == "$":
                pass
            elif isinstance(self.grammar.get_element_by_id(node.name), Terminal):
                try:
                    index = node.token.type.name.find("_")
                    token_type = (node.token.type.name[:index], node.token.type.name)[index == -1]
                    node.name = f"({token_type}, {node.token.lexeme}) "
                except:
                    pass
        with open(path, 'w', encoding='utf-8') as f:
            for pre, fill, node in RenderTree(self.root):
                f.write("%s%s\n" % (pre, node.name))

    def export_syntax_error(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            for line_no, error in self.errors:
                f.write(f"#{line_no} : Syntax Error, {error}\n")
