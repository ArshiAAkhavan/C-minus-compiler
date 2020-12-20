# Scanner
Scanner is the part of the compiler that reads the input file character by character and recognizes tokens. 

If only this phase is implemented, there should be while in [compiler.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/compiler.py) that calls a function in [scanner.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/scanner.py#L16) (get_next_token()) to read the next token from input file; in next phases this function is called by parser.. The get_next_token() function does this by the help of [buffer_reader.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/buffer_reader.py); buffer_reader inputs a file and returns its characters one by one. The line number of the input file is also tracked ,for reporting errors and tokens, by counting the number of "\n"'s in the file.

This scanner recognizes tokens by a structure defined in [lang.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/lang.py). Basically, this structure is a dfa in code; each state is either a middle or final state and has some edges which if the current character is in (include function) or is not in (exclude function) the state is changed to the next defined state. Each state also takes a function as input; if the state is a final state upon entering the state the function is called and if it's a normal state, if the current character can not move to another state by the edges the function is triggered. In this project the functions in [actions.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/actions.py) are used as input functions; these functions either recognize a token in final state cases or generate an error. In the case of final state, the node can push back the last character if needed.

The dfa for this compiler is defined in multiple functions in [default_scanner.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/scanner/default_scanner.py), by passing them the start node of dfa they all become a connected dfa that recognizes the tokens we need.
## Tables
Error Table for lexical errors, Token Table and Symbol Table and additional information can be found in [tables folder](https://github.com/ArshiAAkhavan/C-minus-compiler/tree/master/tables).
## How To Use
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
