# Parser
Parser is the part of the compiler that recognizes the grammar used by the input.

In this project we have a [LL1 class](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L10) that generates the parse table from the grammar and after that by using the function [generate_parse_tree](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L47) parses the input and creates a parse tree that can be printed. This class is also able to recognize different errors by using [panic](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L82) and [add_error](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L36) functions depending on where the error in generating parse tree happened. You can view the syntax errors and parse tree by calling [export_syntax_error](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L121) and [export_parse_tree](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py#L128). In order to create the parse tree [anytree library](https://github.com/c0fec0de/anytree) was used.

## Grammar
[parser.py](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/parser.py) generates the parse table using an instance of [grammar class](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L37). The grammar class reads the information of the grammar(first, follow, rules, predict sets)
from the [data folder](https://github.com/ArshiAAkhavan/C-minus-compiler/tree/master/Parser/data). Note that this works only after making instances of [Terminal](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L1) and [NonTerminal](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L11) classes that are terminals and non-terminals used by the grammar.
## How to Use
This project is an LL1 parser so you can use this project if you have an LL1 grammar. First you should modify the [init_terminals](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L93) and [init_non_terminals](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L101) to containt the elements of your grammar. Then you have to replace the 4 files containing Firsts, Follows, Rules and predic sets in [data folder](https://github.com/ArshiAAkhavan/C-minus-compiler/tree/master/Parser/data). Please note the current formatting of the files or if you want to use a different format modify the import functions starting from [here](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L47) to make sure they work correctly.

The parser will work if you do not provide the first sets as well but make sure to remove [this line](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L124).

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
You can calculate the first, follow and predic sets of your grammar using [this tool](https://mikedevice.github.io/first-follow/).

You also have to modify the [init_terminals](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L93) and [init_non_terminals](https://github.com/ArshiAAkhavan/C-minus-compiler/blob/master/Parser/grammar.py#L101) as shown bellow:

```python
def init_terminals():
    return [Terminal('$'), Terminal('id'), Terminal('*')]

def init_non_terminals():
    return [NonTerminal('E')]
```
