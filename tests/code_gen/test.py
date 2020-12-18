import platform
from code_gen import CodeGen
from scanner.default_scanner import build_scanner
from tables import tables
from Parser.parser import LL1
from Parser.grammar import init_grammar
import logging

grammer = init_grammar()


def main():
    number_of_tests = 10
    test_passes = True
    status = ""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    for i in range(1, number_of_tests + 1, 1):
        prefix = f"tests/code_gen/samples/T{i}/"

        sc = build_scanner(f"{prefix}input.txt")
        parser = LL1(sc, grammer, CodeGen())

        tables.get_token_table().tokens = []
        tables.get_symbol_table().scopes = []
        tables.get_error_table().parse_trees = []

        parser.generate_parse_tree()
        parser.export_code("tests/code_gen/output.txt")



        logger.warning(f"test no.{i}:")
        logger.warning(
            f"\tparse_tree.txt:\t{open('parse_tree.txt').read().strip() == open(f'{prefix}parse_tree.txt').read().strip()}")
        logger.warning(
            f"\tsyntax_errors.txt:\t{open('syntax_errors.txt').read().strip().lower() == open(f'{prefix}syntax_errors.txt').read().strip().lower()}")

        test_status = open('parse_tree.txt').read().strip() == open(
            f'{prefix}parse_tree.txt').read().strip() and open('syntax_errors.txt').read().strip().lower() == open(
            f'{prefix}syntax_errors.txt').read().strip().lower()

        test_passes = test_passes and test_status
        status += ("F", ".")[test_status]

    logger.warning("".ljust(60, "="))
    logger.warning(status)
    logger.warning(("test failed", "test was successful!")[test_passes])


if __name__ == "__main__":
    main()
