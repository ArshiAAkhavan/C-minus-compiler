from collections import namedtuple
from scanner.tokens import Token, TokenType

IDRecord = namedtuple('IDRecord', 'token element_type no_args type scope')

class ScopeStack:
    def __init__(self,parent=None):
        self.stack=[]
        self.parent=parent

    def append(self,token,force=False):
        if force:
            return self.append(token)
        id_record = self.get_IDrecord(token.lexeme)
        if id_record:
            return id_record
        else:
            return self.parent.get_IDrecord(token.lexeme)

    def __append(self,token):
        id_record=IDRecord(token,None,None,None,self)
        self.stack.append(id_record)
        return id_record

    def get_IDrecord(self, lexeme):
        for record in self.stack:
            if record.token.lexeme == lexeme:
                return lexeme
        return None

class __SymbolTable:
    keyword = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]

    def __init__(self):
        self.scopes = []
        self.scopes.append(ScopeStack())

    def new_scope_stack(self):
        self.scopes.append(ScopeStack(self.scopes[-1]))

    def get_current_scope(self):
        return self.scopes[-1]
















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
