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

    def end(self):
        file = open("lexical_errors.txt", "w")
        for e in self.lexical_errors:
            s = str(e.lineno) + ".\t(" + str(e.characters) + ", " + str(e.error_type) + ")\n"
            file.write(s)
        file.close()

class __SymbolTable:
    keyword = ["if", "else", "void", "int", "while", "break", "continue", "switch", "default", "case", "return"]
    def __init__(self):
        self.ids = []
        self.keywords = []

    def add_symbol(self, line_no,token):
        (self.ids,self.keywords)[token.type.__name__ in __SymbolTable.keyword].append((line_no,token))
        return self

    def end(self):
        file = open("symbol_table.txt", "w")
        i = 1
        for e in self.keyword + self.ids:
            s = str(i) + ".\t" + str(e) + "\n"
            file.write(s)
            i += 1
        file.close()

class __TokenTable:
    def __init__(self):
        self.tokes=[]

    def add_token(self,line_no,token):
        self.tokes.append((line_no))

    def __str__(self):
        #todo
        super().__str__(self)


symbol_table=__SymbolTable()
error_table =__ErrorTable()
token_table =__TokenTable()

def get_symbol_table():return symbol_table
def get_token_table():return token_table
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
    s.add_symbol("if").add_symbol("dob").add_symbol("return").add_symbol("if").add_symbol("f7").add_symbol("uio").add_symbol("f7").end()