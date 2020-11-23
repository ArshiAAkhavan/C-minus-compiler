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

In this phase, there should be while in [compiler.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/compiler.py) that calls a function in [scanner.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/scanner.py#L12) (get_next_token()) to read the next character from input file; in next phases this function is called by parser. get_next_token() function does this by the help of [buffer_reader.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/buffer_reader.py); buffer_reader inputs a file and returns its characters one by one. The line number of the input file is also tracked ,for reporting errors and tokens, by counting the number of "\n"'s in the file.

This scanner recognizes tokens by a structure defined in [lang.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/lang.py). Basically, this structure is a dfa in code; each state is either a middle or final state and has some edges which if the current character is in (include function) or is not in (exclude function) the state is changed to the next defined state. Each state also takes a function as input; if the state is a final state upon entering the state the function is called and if it's a normal state, if the current character can not move to another state by the edges the function is triggered. In this project the functions in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py) are used as input functions; these functions either recognize a token in final state cases or generate an error. In the case of final state, the node can push back the last character if needed.

The dfa for this compiler is defined in multiple functions in [compiler.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/compiler.py), by passing them the start node of dfa they all become a connected dfa that recognizes the tokens we need.

### Token Table

Token Table is a singleton class defined in [tables.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/tables.py). This table entries come from the functions in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py) (comments and whitespace are not added into the table because they are not needed in other phases of compiler). Functions in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py) use TokenType class defined in tokens.py to define the token type and create a token. This class has an export function that writes the tokens of each line in "tokens.txt" in a line started by their line number; you can see examples of input and output files (from all tables) in the samples folder.

### Error Table

This compiler implements panic mode error recognition. Error Table is another singleton class in [tables.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/tables.py) which its entries come from the error_gen function in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py). This table contains a list of errors which upon calling its export function writes them into "lexical_errors.txt". Note that error_gen only recognizes errors in tokens and not syntax or semantic errors.

### Symbol Table

Symbol table is another singleton class in [tables.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/tables.py) with entries from [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py) functions. This table has two list; a list initialized by keywords and used for recognizing them from ids and another list for ids. Anytime a new id is seen it is entered in the id list; in this phase only the lexeme is entered. Its export function writes the keywords and ids in "symbol_table.txt".

## Second Phase : Parser
Parser is the part of the compiler that recognizes the grammar used by the input.

In this project we have a [LL1 class](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L9) that generates the parse table from the grammar and after that by using the function [generate_parse_tree](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L45) parses the input and creates a parse tree that can be printed. This class is also able to recognize different errors by using [panic](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L74) and [add_error](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L34) functions depending on where the error in generating parse tree happened. You can view the syntax errors and parse tree by calling [export_syntax_error](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L113) and [export_parse_tree](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L120). In order to create the parse tree [anytree library](https://github.com/c0fec0de/anytree) was used.

### Grammar
[parser.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py) generates the parse table using an instance of [grammar class](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L32). The grammar class reads the information of the grammar(first, follow, rules, predict sets)
from the [data folder](https://github.com/ArshiAAkhavan/C-minus-compiler/tree/master/Parser/data). Note that this works only after making instances of [Terminal](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L1) and [NonTerminal](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L11) classes that are terminals and non-terminals used by the grammar.
## Test
The file [test_scanner.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/tests/scanner/test.py) uses the samples folder to see if the expected outputs are generated by scanner and reports the results in log.
The file [test_parser.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/tests/parser/test.py) does the same for parser.
In order for this files to work correctly the working directory for them has to be changed to the project folder not the folder they are currently in.
## How to Use
### Scanner
If you have a dfa, you can make a scanner by using this project. Scanner inputs are the root of your dfa, a buffer_reader and your language. Buffer reader inputs are the path of your input file and the size of your buffer.

You can create your dfa the same way that we have in [compiler.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/compiler.py) or you can use or modify what we already have. The same goes for functions in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py); you can use what we already have or you can add your own functions as long as they have the same 2 inputs line number and lexeme.

An example of dfa to code:

Here is the example dfa that is for positive integer numbers:

![alt text](https://user-images.githubusercontent.com/45355182/96004173-ef963e80-0e47-11eb-9b04-69e31c037756.png "NUMBER DFA")

Here let's assume that the only error is Invalid Input (The Error and Error Table classes have been defined in [tables.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/tables.py)):

```python
def error(line_no, lexeme):
  error = tables.Error(line_no, lexeme, "Invalid input")
  tables.get_error_table().add_lexical_error(error)
```

We also need another function for accept state (Token and TokenTypes are defined in [tokens.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/tokens.py) and Token Table is defined in [tables.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/tables.py)):

```python
def num_token_gen(line_no,lexeme): 
    token=Token(TokenType.NUM, lexeme)
    tables.token_table.add_token(line_no,token)
    return token
```

This function is already available in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py).

Now we get to the states. To make the start state S1:

```python
S1 = DFANode(error)
```

This will create a normal node that calls the error function if it doesn't have any edges fitting the current character.

S2 is made in the same way:

```python
S2 = DFANode(error)
```

S3 is a final state:

```python
S3 = FinalStateNode(num_token_gen, True)
```

The True input is showing that we do not need the other character in our number token; it is the start of another token (or an error) so after reaching the final state it is pushed back. If in a dfa the last character doesn't need to be pushed back the second input should be False. The function in a final state is called when the state is entered and after tokenizing number, Scanner goes back to start state.

Now we have to connect the nodes to each other:

```python
# the outward edges of S1
S1.append(Edge().include("0", "9"), S2)
# the outward edges of S2
num_middle_state.append(Edge().include("0", "9"), num_middle_state).append(Edge().exclude("0", "9"), S3)
```

S2 has both include and exclude edges. Also if there are more things that need to be excluded in an edge it can be done like this:

```python
num_middle_state.append(Edge().include("0", "9"), num_middle_state).append(Edge().exclude("0", "9").exclude("a", "z").exclude("A", "Z"), num_final_state)
```

The number of edges is not limited; append can be called more than twice.

Scanner is given an edge called language as input; at any point if a character is not in the language edge the scanner calles the [error generator function](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py#L22). If there is a state that needs to recognize characters that are not in the language (like comments) it can be done via an optional input in DFANode constructer:

```python
comment_start_state = DFANode(actions.error_gen,supports_all_langs=True) 
```
### Parser
This project is an LL1 parser so you can use this project if you have an LL1 grammar. First you should modify the [init_terminals](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L87) and [init_non_terminals](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L95) to containt the elements of your grammar. Then you have to replace the 4 files containing Firsts, Follows, Rules and predic sets in [data folder](https://github.com/ArshiAAkhavan/C-minus-compiler/tree/master/Parser/data). Please note the current formatting of the files or if you want to use a different format modify the import functions starting from [here](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L42) to make sure they work correctly.

The parser will work if you do not provide the first sets as well but make sure to remove [this line](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L118).

Here is a simple example:

```
E -> id * id $
```

The above will be the content of [grammar.txt](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/data/grammar.txt).

For the other files we have:

```
Firsts.txt:

E id

Follow.txt:

E

Predicts.txt:

id
```

You also have to modify the [init_terminals](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L87) and [init_non_terminals](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L95) as shown bellow:

```python
def init_terminals():
    return [Terminal('$'), Terminal('id'), Terminal('*')]

def init_non_terminals():
    return [NonTerminal('E')]
```
