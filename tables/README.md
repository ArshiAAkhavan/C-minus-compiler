
### Token Table

Token Table is a singleton class defined in [tables.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/tables/tables.py#L29). This table entries come from scanner by the functions in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py) (comments and whitespace are not added into the table because they are not needed in other phases of compiler). Functions in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py) use TokenType class defined in tokens.py to define the token type and create a token. This class has an export function that writes the tokens of each line in "tokens.txt" in a line started by their line number; you can see examples of input and output files (from all tables) in the samples folder.

### Error Table

This compiler implements panic mode error recognition. Error Table is another singleton class in [tables.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/tables/tables.py#L11) which its entries come from the error_gen function in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py). This table contains a list of lexical errors (errors discovered by the scanner) which upon calling its export function writes them into "lexical_errors.txt". Note that error_gen only recognizes errors in tokens and not syntax or semantic errors.

### Symbol Table

Symbol table is another singleton class in [symbolTable.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/tables/symbolTable.py#L47) with entries from [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py) functions. This table has two list; a list initialized by keywords and used for recognizing them from ids and another list for ids. Anytime a new id is seen it is entered in the id list; in this phase only the lexeme is entered. Its export function writes the keywords and ids in "symbol_table.txt".
