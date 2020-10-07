class Error:
    def __init__(self, lineno, characters, error_type):
        self.lineno = lineno
        self.characters = characters
        self.error_type = error_type


class ErrorTable:
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


class SymbolTable:
    def __init__(self):
        self.keyword = ["if", "else", "void", "int", "while", "break", "continue", "switch", "default", "case", "return"]
        self.id = []

    def add_symbol(self, string):
        if string not in self.keyword + self.id:
            self.id.append(string)
        return self

    def end(self):
        file = open("symbol_table.txt", "w")
        i = 1
        for e in self.keyword + self.id:
            s = str(i) + ".\t" + str(e) + "\n"
            file.write(s)
            i += 1
        file.close()


if __name__ == "__main__":
    # e = ErrorTable()
    # err1 = Error(3, "an@", "Invalid Input")
    # err2 = Error(5, "so!", "Invalid Input")
    # err3 = Error(6, "3d", "Invalid number")
    # e.add_lexical_error(err1)
    # e.add_lexical_error(err2)
    # e.add_lexical_error(err3)
    # e.end()
    s = SymbolTable()
    s.add_symbol("if").add_symbol("dob").add_symbol("return").add_symbol("if").add_symbol("f7").add_symbol("uio").add_symbol("f7").end()