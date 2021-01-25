import os
import platform
from code_gen import CodeGen
from scanner.default_scanner import build_scanner
from scanner.tokens import Token, TokenType
from tables import tables
from Parser.parser import LL1
from Parser.grammar import init_grammar
import logging

grammar = init_grammar()
test_command = {"Linux": "chmod +x tests/code_gen/Linux.out && tests/code_gen/Linux.out > expected.txt 2>/dev/null",
                "Darwin": "chmod +x tests/code_gen/Mac.out && tests/code_gen/Mac.out > expected.txt 2>/dev/null",
                "Windows": "{0}/tests/code_gen/Windows.exe > expected.txt 2> NUL".format(os.getcwd().replace('\\', '/')),
                }


def main():
    number_of_tests = 27
    test_passes = True
    status = ""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    for i in range(1, number_of_tests + 1, 1):
        prefix = f"tests/code_gen/samples/T{i}/"

        sc = build_scanner(f"{prefix}input.txt")
        parser = LL1(sc, grammar, CodeGen())

        tables.get_token_table().tokens = []
        tables.get_symbol_table().clear()
        tables.symbol_table.add_symbol(Token(TokenType.ID, "output"))
        tables.symbol_table.fetch("output").address = 5

        tables.get_error_table().parse_trees = []

        parser.generate_parse_tree()
        parser.code_gen.execute_from("main")
        parser.export_code("output.txt")
        os.system(test_command[platform.system()])
        logger.warning(f"test no.{i}:")
        logger.warning(
            f"\texpected.txt:\t{open('expected.txt').read().strip() == open(f'{prefix}expected.txt').read().strip()}")

        test_status = open('expected.txt').read().strip() == open(f'{prefix}expected.txt').read().strip()

        test_passes = test_passes and test_status
        status += ("F", ".")[test_status]

    logger.warning("".ljust(60, "="))
    logger.warning(status)
    logger.warning(("test failed", "test was successful!")[test_passes])


if __name__ == "__main__":
    main()
