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
            for e in self.lexical_errors:
                s=f"{e.lineno}.\t({e.characters}, {e.error_type})\n"
                file.write(s)
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
        for i, e in enumerate(self.keyword + self.ids):
            s = f"{i+1}.\t{e}\n"
            file.write(s)
        file.close()


class __TokenTable:
    def __init__(self):
        self.tokens = []

    def add_token(self, line_no, token):
        self.tokens.append((line_no, token))

    def export(self,path):
        # file= open(path,"w")
        # self.tokens.sort(lambda row: row[0])
        # print(self.tokens)
        pass
    def __str__(self):
        return "\n".join([f"{line_no}:\t\t<{token.type.name},{token.lexeme}>" for line_no,token in self.tokens])


symbol_table = __SymbolTable()
error_table = __ErrorTable()
token_table = __TokenTable()


def get_symbol_table(): return symbol_table


def get_token_table(): return token_table


def get_error_table(): return error_table


if __name__ == "__main__":

    # e = __ErrorTable()
    # err1 = Error(3, "an@", "Invalid Input")
    # err2 = Error(5, "so!", "Invalid Input")
    # err3 = Error(6, "3d", "Invalid number")
    # e.add_lexical_error(err1)
    # e.add_lexical_error(err2)
    # e.add_lexical_error(err3)
    # e.end()
    s = get_symbol_table()
    s.add_symbol(Token(TokenType.ID, "heshmat"))
    print(get_symbol_table())
    s.add_symbol("if").add_symbol("dob").add_symbol("return").add_symbol(
        "if").add_symbol("f7").add_symbol("uio").add_symbol("f7").end()
