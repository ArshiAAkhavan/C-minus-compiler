from scanner.tokens import Token, TokenType
from tables import tables


def num_token_gen(line_no, lexeme):
    token = Token(TokenType.NUM, lexeme)
    tables.token_table.add_token(line_no, token)
    return token


def id_token_gen(line_no, lexeme):
    token = tables.get_symbol_table().add_symbol(Token(TokenType.ID, lexeme))
    tables.token_table.add_token(line_no, token)
    return token


def symbol_token_gen(line_no, lexeme):
    token = Token(TokenType(sum(ord(c) for c in lexeme)), lexeme)
    tables.get_token_table().add_token(line_no, token)
    return token


def comment_token_gen(line_no, lexeme): return Token(TokenType.COMMENT, lexeme)


def whitespace_token_gen(line_no, lexeme):
    if lexeme == chr(26):
        return Token(TokenType.EOF, "$")
    else:
        return Token(TokenType.WHITE_SPACE, lexeme)


def error_gen(line_no, lexeme):
    if 57 >= ord(lexeme[0]) >= 48 and (
            91 > ord(lexeme[len(lexeme) - 1]) > 64 or 123 > ord(lexeme[len(lexeme) - 1]) > 96):
        error = tables.Error(line_no, lexeme, "Invalid number")
        tables.get_error_table().add_lexical_error(error)
    elif lexeme.startswith("/*"):
        if len(lexeme) < 8:
            error = tables.Error(line_no, lexeme, "Unclosed comment")
        else:
            error = tables.Error(line_no, lexeme[0:7] + "...", "Unclosed comment")
        tables.get_error_table().add_lexical_error(error)
    elif lexeme == "*/":
        error = tables.Error(line_no, lexeme, "Unmatched comment")
        tables.get_error_table().add_lexical_error(error)
    else:
        error = tables.Error(line_no, lexeme, "Invalid input")
        tables.get_error_table().add_lexical_error(error)
    return Token(TokenType.ERROR, lexeme)
