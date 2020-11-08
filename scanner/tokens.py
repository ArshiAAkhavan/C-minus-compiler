from collections import namedtuple
from enum import Enum


class TokenType(Enum):
    NULL = 0                        # 0000000       Null
    ID = 1                          # 0000001       abcd...xyz
    KEYWORD = 2                     # 0000001       abcjanad...xyz
    NUM = 3                         # 0000010       0123456789
    WHITE_SPACE = 4                 # 0000011       \n\t\r\v\f
    COMMENT = 5                     # 0000100       // /**/
    ERROR = 6                       # 0000110       needed for parser flow
    EOF = 26                        # 0011010       $

    SYMBOL_LT = 60                  # 0111100       <
    SYMBOL_AS = 61                  # 0111101       =
    SYMBOL_EQ = 122                 # 1111000       ==

    SYMBOL_MUL = 42                 # 0101010       *
    SYMBOL_ADD = 43                 # 0101011       +
    SYMBOL_SUB = 45                 # 0101111       -

    SYMBOL_COMMA = 44               # 0101110       ,
    SYMBOL_COLON = 58               # 0111010       :
    SYMBOL_SEMI_COLON = 59          # 0111011       ;

    SYMBOL_BRACKET_O = 91           # 1011011       [
    SYMBOL_BRACKET_C = 93           # 1011101       ]
    SYMBOL_PARENTHESIS_O = 40       # 0101000       (
    SYMBOL_PARENTHESIS_C = 41       # 0101001       )
    SYMBOL_CURLY_BRACKET_O = 123    # 1111011       {
    SYMBOL_CURLY_BRACKET_C = 125    # 1111101       }


Token = namedtuple('Token', 'type lexeme')
