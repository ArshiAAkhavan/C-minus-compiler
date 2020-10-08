from tokens import Token
from tokens import TokenType
import tables 

def num_token_gen(line_no,lexeme): 
    token=Token(TokenType.NUM, lexeme)
    tables.token_table.add_token(line_no,token)
    return token

def id_token_gen(line_no,lexeme): 
    token=tables.get_symbol_table().add_symbol(Token(TokenType.ID, lexeme))
    tables.token_table.add_token(line_no,token)
    return token

def symbol_token_gen(line_no,lexeme): 
    token=Token(TokenType(sum(ord(c) for c in lexeme)), lexeme)
    tables.get_token_table().add_token(line_no,token)
    return token

def comment_token_gen(line_no,lexeme):return Token(TokenType.COMMENT, lexeme)
def whitespace_token_gen(line_no,lexeme): return Token(TokenType.WHITE_SPACE, lexeme)

def error_gen(line_no,lexeme):
    pass
