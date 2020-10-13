# C-mnius Compiler

**a Python3 based one-pass compiler for a very simplified C-minus**

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
Scanner is the part of the compiler that reads the input file character by character and recognizes tokens.

In this project, the preassumption is that a file called "input.txt" contains the code and is in the same directory as compiler.py.

In this phase, there is a while in compiler.py that calls a function in Scanner/Scanner.py (get_next_token()) to read the next character from input file; in future phases this function will be called by parser. get_next_token() function does this by the help of buffer_reader.py; buffer_reader inputs a file and returns its characters one by one. The line number of the input file is also tracked ,for reporting errors and tokens, by counting the number of "\n"'s in the file.

This scanner recognizes tokens by a structure defined in lang.py. Basically, this structure is a dfa in code; each state is either a middle or final state and has some edges which if the current character is in (include function) or is not in (exclude function) the state is changed to the next defined state. Each state also takes a function as input; if the state is a final state upon entering the state the function is called and if it's a normal state, if the current character can not move to another state by the edges the function is triggered. In this project the functions in action.py are used as input functions; these functions either recognize a token in final state cases or generate an error. In the case of final state, the node can push back the last character if needed.

The dfa for this compiler is defined in multiple functions in compiler.py, by passing them the start node of dfa they all become a connected dfa that recognizes the tokens we need.

### Token Table

Token Table is a singleton class defined in tables.py. This table entries come from the functions in action.py (comments and whitespace are not added into the table because they are not needed in other phases of compiler). Functions in action.py use TokenType class defined in tokens.py to define the token type and create a token. This class has an export function that writes the tokens of each line in "tokens.txt" in a line started by their line number; you can see examples of input and output files (from all tables) in the samples folder.

### Error Table

This compiler implements panic mode error recognition. Error Table is another singleton class in tables.py which its entries come from the error_gen function in actions.py. This table contains a list of errors which upon calling its export function writes them into "lexical_errors.txt". Note that error_gen only recognizes errors in tokens and not syntax or semantic errors.

### Symbol Table

Symbol table is another singleton class in tables.py with entries from action.py functions. This table has two list; a list initialized by keywords and used for recognizing them from ids and another list for ids. Anytime a new id is seen it is entered in the id list; in this phase only the lexeme is entered. Its export function writes the keywords and ids in "symbol_table.txt".

## Test Scanner
The file test_scanner.py uses the samples folder to see if the expected outputs are generated from each input and reports the results in log.
### How to Use
If you have a dfa, you can make a scanner by using this project. Scanner inputs are the root of your dfa, a buffer_reader and your language. Buffer reader inputs are the path of your input file and the size of your buffer.
You can create your dfa the same way that we have in compiler.py
