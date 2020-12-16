from collections import namedtuple
from scanner.tokens import Token, TokenType

IDRecord = namedtuple('IDRecord', 'token element_type no_args type scope')


class __SymbolTable:
    keyword = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]

    def __init__(self):
        self.scopes = []
        self.new_stack()

    def add_symbol(self, token, is_declaration=False):
        if token.lexeme in self.keyword:
            return Token(TokenType.KEYWORD, token.lexeme)
        elif token.lexeme not in self.ids:
            self.ids.append(token.lexeme)
        return token


















    def __str__(self):
        s = ""
        for i, t in enumerate(self.keyword + self.ids):
            s += f"{i}.\t{t}\n"
        return s

    def export(self, path):
        file = open(path, "w")
        for i, e in enumerate(self.keyword + self.ids):
            file.write(f"{i + 1}.\t{e}")
            if i < len(self.keyword + self.ids) - 1:
                file.write("\n")
        file.close()
=======
        else:
            return self.add_id(token, is_declaration)

    def new_stack(self):
        self.scopes.append([])

    def add_id(self, token, is_declaration):
        if is_declaration:
            record = self.fetch(token, 1)
            if record is None:
                return self.add_record(token)
            else:
                return record.token

    def fetch(self, token, depth=0):
        if depth == 0: depth = len(self.scopes)

        for scope in self.scopes.reverse():
            record = self.fetch_in_scope(self, token)
            if record is not None:return 

        return None

    def add_record(self, token):
        record = IDRecord(token.lexeme, '', '', '', len(self.scope_stacks))
>>>>>>> Stashed changes
