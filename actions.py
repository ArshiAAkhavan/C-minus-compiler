from tokens import Token
from tokens import TokenType
import tables 

def num_token_gen(line_no,lexeme): return Token(TokenType.NUM, lexeme)
def id_token_gen(line_no,lexeme): 
    token=Token(TokenType.ID, lexeme)
    tables.get_symbol_table().add_symbol(line_no,token)

def comment_token_gen(line_no,lexeme): return Token(TokenType.COM, lexeme)
def whitespace_token_gen(line_no,lexeme): return Token(TokenType.WS, lexeme)
def symbol_token_gen(line_no,lexeme): return Token(TokenType(sum(ord(c) for c in lexeme)), lexeme)


def error_gen(line_no,lexeme):
    pass
