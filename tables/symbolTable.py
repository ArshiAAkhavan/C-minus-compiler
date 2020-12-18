from scanner.tokens import Token, TokenType


# IDRecord = namedtuple('IDRecord', 'token element_type no_args type scope address')
# todo      i needed IDRecord to be mutable so i coudlnt used namedTuple but we can alternate that with RecordClass
# todo      since in this project we can not use any external library then i am forced to use class instead
# todo      currect implementation: from recordclass import recordclass
#                                   IDRecord = recordclass('IDRecord', 'token element_type no_args type scope address')
class IDRecord:
    def __init__(self, token=None, element_type=None, no_args=None, id_type=None, scope=None, address=None):
        self.token = token
        self.element_type = element_type
        self.no_args = no_args
        self.id_type = id_type
        self.scope = scope
        self.address = address


class Scope:
    def __init__(self, parent=None):
        self.stack = []
        self.parent = parent

    def append(self, token, force=False):
        if force:
            return self.__append(token)
        id_record = self.get_IDrecord(token.lexeme)
        if id_record:
            return id_record
        else:
            return self.__append(token)

    def __append(self, token):
        id_record = IDRecord(token, None, None, None, self, None)
        self.stack.append(id_record)
        return id_record

    def get_IDrecord(self, lexeme):
        for record in self.stack:
            if record.token.lexeme == lexeme:
                return record
        if self.parent:
            return self.parent.get_IDrecord(lexeme)
        return None


class __SymbolTable:
    keyword = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]

    def __init__(self):
        self.scopes = []
        self.ids = []
        self.scopes.append(Scope())

    def clear(self):
        self.scopes = []
        self.ids = []
        self.scopes.append(Scope())

    def new_scope(self):
        self.scopes.append(Scope(self.scopes[-1]))

    def remove_scope(self):
        self.scopes.pop()

    def get_current_scope(self):
        return self.scopes[-1]

    def add_symbol(self, token, is_declaration=False):
        if token.lexeme in self.keyword:
            return Token(TokenType.KEYWORD, token.lexeme)
        self.get_current_scope().append(token, is_declaration)
        return token

    def fetch(self, lexeme):
        return self.get_current_scope().get_IDrecord(lexeme)

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
