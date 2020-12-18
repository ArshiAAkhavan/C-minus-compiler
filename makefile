SHELL := /bin/bash

dev:
	python3 compiler.py

test_scanner:
	export PYTHONPATH="./" && python3 tests/scanner/test.py
test_parser:
	export PYTHONPATH="./" && python3 tests/parser/test.py
test_code_gen:
	export PYTHONPATH="./" && python3 tests/code_gen/test.py
test_version:
	export PYTHONPATH="./" && which python
