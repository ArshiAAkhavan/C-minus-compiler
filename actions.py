from tokens import Token
from tokens import TokenType
from Tables import SymbolTable

def num_token_gen(lexeme): return Token(TokenType.NUM, lexeme)
def id_token_gen(lexeme): 
    token=Token(TokenType.ID, lexeme)
    SymbolTable.append(token)

def comment_token_gen(lexeme): return Token(TokenType.COM, lexeme)
def whitespace_token_gen(lexeme): return Token(TokenType.WS, lexeme)
def symbol_token_gen(lexeme): return Token(TokenType(sum(ord(c) for c in lexeme)), lexeme)


def error_gen(lexeme):
    pass
