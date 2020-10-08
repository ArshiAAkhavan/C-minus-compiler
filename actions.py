from tokens import Token
from tokens import TokenType


num_token_gen       = lambda lexeme:Token(TokenType.NUM,lexeme)
id_token_gen        = lambda lexeme:Token(TokenType.ID ,lexeme)    
comment_token_gen   = lambda lexeme:Token(TokenType.COM,lexeme)    
whitespace_token_gen= lambda lexeme:Token(TokenType.WS ,lexeme)
symbol_token_gen    = lambda lexeme:Token(TokenType(sum(ord(c) for c in lexeme)),lexeme)

def error_gen(lexeme):
    pass
