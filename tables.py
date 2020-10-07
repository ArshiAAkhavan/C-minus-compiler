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
        self.symbols = []

    def add_symbol(self, string):
        if string not in self.symbols:
            self.symbols.append(string)
        return {
            'if': True,
            'else': True,
            'void': True,
            'int': True,
            'while': True,
            'break': True,
            'switch': True,
            'default': True,
            'case': True,
            'return': True
        }.get(string, False)

    def end(self):
        file = open("symbol_table.txt", "w")
        i = 1
        for e in self.symbols:
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
    print(s.add_symbol("if"))
    print(s.add_symbol("dob"))
    print(s.add_symbol("return"))
    print(s.add_symbol("if"))
    s.end()