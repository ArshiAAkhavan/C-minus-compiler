from tokens import *


class Error:
    def __init__(self, lineno, characters, error_type):
        self.lineno = lineno
        self.characters = characters
        self.error_type = error_type


class __ErrorTable:
    def __init__(self):
        self.lexical_errors = []

    def add_lexical_error(self, error):
        self.lexical_errors.append(error)

    def export(self,path):
        file = open(path, "w")
        if not self.lexical_errors:
            file.write("There is no lexical error.")
        else:
            [file.write(f"{e.lineno}.\t({e.characters}, {e.error_type})\n") for e in self.lexical_errors]
        file.close()


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
        for i, t in enumerate(self.keyword+self.ids):
            s += f"{i}.\t{t}\n"
        return s

    def export(self,path):
        file = open(path, "w")
        [file.write(f"{i+1}.\t{e}\n") for i, e in enumerate(self.keyword + self.ids)]
        file.close()


class __TokenTable:
    def __init__(self):
        self.tokens = []

    def add_token(self, line_no, token):
        self.tokens.append((line_no, token))

    def export(self,path):
        file= open(path,"w")
        current_line_no=-1
        for line_no,token in self.tokens:
            if current_line_no != line_no:
                current_line_no=line_no
                file.write(f"\n{line_no}")
            index=token.type.name.find("_")
            token_type=(token.type.name[:index],token.type.name)[index==-1]
            file.write(f"({token_type}, {token.lexeme}) ")

    def __str__(self):
        return "\n".join([f"{line_no}:\t\t<{token.type.name},{token.lexeme}>" for line_no,token in self.tokens])


symbol_table = __SymbolTable()
error_table = __ErrorTable()
token_table = __TokenTable()
def get_symbol_table(): return symbol_table
def get_token_table(): return token_table
def get_error_table(): return error_table

