class TokenMissMatchException(Exception):
    def __init__(self, token_lexeme):
        super(TokenMissMatchException, self).__init__(
            f"could not match lexeme[{token_lexeme}] with any known regular expressions...")
        self.token_lexeme=token_lexeme
class InvalidInputException(Exception):
    def __init__(self, character):
        super(InvalidInputException, self).__init__(
            f"no token starts with character:[{character}]")
        self.token_lexeme=character

class InvalidNumberTokenException(Exception):
    def __init__(self, token_lexeme):
        super(InvalidNumberTokenException, self).__init__(
            f"invalid format for number:[{token_lexeme}]")
        self.token_lexeme=token_lexeme

class UnClosedCommentException(Exception):
    def __init__(self, token_lexeme):
        super(UnClosedCommentException, self).__init__(
            f"comment not closed:[{token_lexeme}]")
        self.token_lexeme=token_lexeme

class UnMatchedCommentException(Exception):
    def __init__(self, token_lexeme):
        super(UnMatchedCommentException, self).__init__(
            f"lexeme [{token_lexeme}]has no starting point")
        self.token_lexeme=token_lexeme

class NotEnoughCharacterException(Exception):
    def __init__(self, token_lexeme):
        super(NotEnoughCharacterException, self).__init__(
            f"failed to generete new token due to lack of characters \
            \nit may be that the input file ended before the we could generate a new token \
            \nfailed lexeme: {token_lexeme}")
        self.token_lexeme=token_lexeme

