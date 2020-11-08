from anytree import Node, RenderTree, PreOrderIter
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

    def add_error(self, error_root, error_type):
        if error_type.lower() == "missing":
            self.errors.append((self.token_generator.get_line_no(), f"{error_type} {error_root.name}"))
        elif error_type.lower() == "illegal":
            if error_root.type is TokenType.EOF:
                self.errors.append((self.token_generator.get_line_no(), f"unexpected {error_root.type.name}"))
            elif error_root.type in [TokenType.NUM, TokenType.ID]:
                self.errors.append((self.token_generator.get_line_no(), f"{error_type} {error_root.type.name}"))
            else:
                self.errors.append((self.token_generator.get_line_no(), f"{error_type} {error_root.lexeme}"))

    def generate_parse_tree(self):
        self.stack = [self.root]
        token = self.get_next_valid_token()
        stack_top = None
        try:
            while len(self.stack):
                stack_top = self.get_next_valid_stack_top()
                stack_top.token = token
                if self.grammar.is_terminal(stack_top.name):  # terminal
                    if stack_top.name != self.get_token_key(token):  # not matching
                        self.add_error(stack_top, "missing")
                        self.remove_top(stack_top)
                    elif len(self.stack):
                        token = self.get_next_valid_token()
                else:  # none_terminal
                    key = (stack_top.name, self.get_token_key(token))
                    if key in self.p_table and self.p_table[key] != "synch":
                        self.update_stack(stack_top, key)
                    else:
                        token = self.panic(stack_top, key, token)
        except NoTokenLeftException:
            self.remove_top(stack_top)
            [self.remove_top(g) for g in self.stack]

        return self.root

    def update_stack(self, stack_top, key):
        self.stack.extend([Node(g, parent=stack_top) for g in self.p_table[key]][::-1])

    def panic(self, stack_top, key, token):
        while key not in self.p_table:
            self.add_error(token, "illegal")
            token = self.get_next_valid_token()
            key = (stack_top.name, self.get_token_key(token))
        if self.p_table[key] != 'synch':
            self.update_stack(stack_top, key)
            return token

        self.add_error(stack_top, "missing")
        self.remove_top(stack_top)
        return token

    def get_next_valid_token(self):
        try:
            token = self.token_generator.get_next_token()
            while token.type in [TokenType.COMMENT, TokenType.WHITE_SPACE, TokenType.ERROR]:
                token = self.token_generator.get_next_token()
            return token
        except Exception:
            raise NoTokenLeftException()

    def get_next_valid_stack_top(self):
        stack_top = self.stack.pop()
        while len(self.stack) and stack_top.name == "ε":
            stack_top = self.stack.pop()
        return stack_top

    @staticmethod
    def get_token_key(token):
        return (token.lexeme, token.type.name)[token.type in [TokenType.NUM, TokenType.ID]]

    @staticmethod
    def remove_top(stack_top):
        if stack_top.parent:
            children = list(stack_top.parent.children)
            children.remove(stack_top)
            stack_top.parent.children = tuple(children)

    def export_parse_tree(self, path):
        for node in PreOrderIter(self.root):
            if node.name == "ε":
                node.name = "epsilon"
            elif node.name != "$" and self.grammar.is_terminal(node.name):
                try:
                    index = node.token.type.name.find("_")
                    token_type = (node.token.type.name[:index], node.token.type.name)[index == -1]
                    node.name = f"({token_type}, {node.token.lexeme}) "
                except:
                    pass
        with open(path, 'w', encoding='utf-8') as f:
            for pre, _, node in RenderTree(self.root):
                f.write("%s%s\n" % (pre, node.name))

    def export_syntax_error(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            if not self.errors:
                f.write("There is no syntax error.\n")
            for line_no, error in self.errors:
                f.write(f"#{line_no} : syntax error, {error}\n")
