# C-mnius Compiler

**a Python3 based compiler for a very simplified C-minus**

## Token types

The tokens in the below table can be recognized by the compiler:
**Token Type** | **Description**
:-------------:|:--------------:
NUM | Any string matching [0-9]+
ID | Any string matching: [A-Za-z][A-Za-z0-9]*
KEYWORD | if, else, void, int, while, break, switch, default, case, return
SYMBOL | ; : , [ ] ( ) { } + - * = < ==
COMMENT | Any string between a /* and a */ OR any string after a // and before a \n or EOF
WHITESPACE | blank (ASCII 32), \n (ASCII 10), \r (ASCII 13), \t (ASCII 9), \v (ASCII 11), \f (ASCII 12)

## First Phase : Scanner
