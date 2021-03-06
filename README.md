# C-mnius Compiler

**a Python3 based one-pass compiler for a very simplified C-minus**

## Token Types and Grammar

The tokens in the below table can be recognized by the compiler:
**Token Type** | **Description**
:-------------:|:--------------:
NUM | Any string matching [0-9]+
ID | Any string matching: [A-Za-z][A-Za-z0-9]*
KEYWORD | if, else, void, int, while, break, switch, default, case, return
SYMBOL | ; : , [ ] ( ) { } + - * = < ==
COMMENT | Any string between a /* and a */ OR any string after a // and before a \n or EOF
WHITESPACE | blank (ASCII 32), \n (ASCII 10), \r (ASCII 13), \t (ASCII 9), \v (ASCII 11), \f (ASCII 12)

The grammar that this compiler uses is in [grammar.txt](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/data/grammar.txt).

## First Phase : Scanner
Scanner is the part of the compiler that reads the input file character by character and recognizes tokens.
In this project, the preassumption is that a file called "input.txt" contains the code and is in the same directory as [compiler.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/compiler.py). 

For additional information and how to use please refer to [here](https://github.com/ArshiAAkhavan/C-minus-compiler/edit/master/scanner/README.md).
## Tables
Error Table for lexical errors, Token Table and Symbol Table and additional information can be found in [tables folder](https://github.com/ArshiAAkhavan/C-minus-compiler/tree/master/tables).

## Second Phase : Parser
Parser is the part of the compiler that recognizes the grammar used by the input.

This project implements a LL1 parser. Additional information and how to use can be viewed in [README of Parser](https://github.com/ArshiAAkhavan/C-minus-compiler/edit/master/Parser/README.md).

## Test
The file [test_scanner.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/tests/scanner/test.py) uses the samples folder to see if the expected outputs are generated by scanner and reports the results in log.
The file [test_parser.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/tests/parser/test.py) does the same for parser.
In order for this files to work correctly the working directory for them has to be changed to the project folder not the folder they are currently in.
## How to Use
### Scanner
Information on how to use and personalize Scanner can be found [here](https://github.com/ArshiAAkhavan/C-minus-compiler/edit/master/scanner/README.md).
### Parser
Information on how to use and personalize Parser can be found [here](https://github.com/ArshiAAkhavan/C-minus-compiler/edit/master/Parser/README.md).
