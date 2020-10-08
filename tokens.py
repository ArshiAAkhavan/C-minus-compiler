
from collections import namedtuple
from enum import Enum

class Token_type(Enum):
    NULL=0                      # 000000        Null
    ID=1                        # 000001        abcd...xyz
    KEY_WORD=1                  # 000001        abcd...xyz
    NUM=2                       # 000010        0123456789
    WHITE_SPACE=3               # 000011        \n\t\r\v\f 
    COMMENT=4                   # 000100        // /**/
    
    SYMBOL_EQ=64                # 100000        ==
    SYMBOL_LT=65                # 100001        <
    SYMBOL_AS=66                # 100010        =
    
    SYMBOL_MUL=68               # 100100        *
    SYMBOL_ADD=69               # 100101        +
    SYMBOL_SUB=70               # 100110        -

    SYMBOL_SEMI_COLON=72        # 101000        ;
    SYMBOL_COLON=73             # 101001        :
    SYMBOL_COMMA=74             # 101010        ,

    SYMBOL_BRACKET_O=96         # 110000        [
    SYMBOL_BRACKET_C=97         # 110001        ]
    SYMBOL_PARENTHESIS_O=98     # 110010        (
    SYMBOL_PARENTHESIS_C=99     # 110011        )
    SYMBOL_CURLY_BRACKET_O=100  # 110100        {
    SYMBOL_CURLY_BRACKET_C=101  # 110101        }

Token = namedtuple('Token', 'type lexeme')

