from scanner.default_scanner import build_scanner
from tables import tables
from scanner import actions
from scanner.buffer_reader import BufferReader
from scanner.scanner import Scanner
from scanner.lang import DFANode, FinalStateNode, Edge
import logging

def main():
    number_of_tests = 17
    test_passes = True
    status = ""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    for i in range(1, number_of_tests + 1, 1):
        prefix = "tests/scanner/samples/T{0:02d}/".format(i)
        sc = build_scanner(f"{prefix}input.txt")

        tables.get_token_table().tokens = []
        tables.get_symbol_table().ids = []
        tables.get_error_table().lexical_errors = []

        while sc.can_generate_token():
            try:
                sc.get_next_token()
            except Exception as e:
                print(e)

        tables.get_error_table().export("lexical_errors.txt")
        tables.get_symbol_table().export("symbol_table.txt")
        tables.get_token_table().export("tokens.txt")

        logger.warning(f"test no.{i}:")
        logger.warning(
            f"\tlexical_error.txt:\t{open('lexical_errors.txt').read().strip() == open(f'{prefix}lexical_errors.txt').read().strip()}")
        logger.warning(
            f"\tsymbol_table.txt:\t{open('symbol_table.txt').read().strip() == open(f'{prefix}symbol_table.txt').read().strip()}")
        logger.warning(
            f"\ttokens.txt:\t\t{open('tokens.txt').read().strip() == open(f'{prefix}tokens.txt').read().strip()}")

        test_status = open('lexical_errors.txt').read().strip() == open(
            f'{prefix}lexical_errors.txt').read().strip() and \
                      open('symbol_table.txt').read().strip() == open(
            f'{prefix}symbol_table.txt').read().strip() and \
                      open('tokens.txt').read().strip() == open(f'{prefix}tokens.txt').read().strip()
        test_passes = test_passes and test_status
        status += ("F", ".")[test_status]

    logger.warning("".ljust(60, "="))
    logger.warning(status)
    logger.warning(("test failed", "test was successful!")[test_passes])


if __name__ == "__main__":
    main()
