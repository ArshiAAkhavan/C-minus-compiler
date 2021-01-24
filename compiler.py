from Parser import init_grammar
from Parser.parser import LL1
from code_gen import CodeGen
from scanner.default_scanner import build_scanner
from tables import tables


# Arshia Akhavan 97110422
# Ghazal Shenavar 97101897



parser = LL1(build_scanner("input.txt"), init_grammar(), CodeGen())

parser.generate_parse_tree()
parser.export_parse_tree("parse_tree.txt")

parser.code_gen.execute_from("main")
parser.export_code("output.txt")

parser.export_syntax_error("syntax_errors.txt")
tables.get_error_table().export("lexical_errors.txt")
# tables.get_symbol_table().export("symbol_table.txt")
tables.get_token_table().export("tokens.txt")
