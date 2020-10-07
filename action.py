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



if __name__ == "__main__":
    e = ErrorTable()
    err1 = Error(3, "an@", "Invalid Input")
    err2 = Error(5, "so!", "Invalid Input")
    err3 = Error(6, "3d", "Invalid number")
    e.add_lexical_error(err1)
    e.add_lexical_error(err2)
    e.add_lexical_error(err3)
    e.end()