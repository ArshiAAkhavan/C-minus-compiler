from scanner.tokens import Token, TokenType


class __SymbolTable:
    keyword = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]

    def __init__(self):
        self.ids = []

    def add_symbol(self, token):
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
