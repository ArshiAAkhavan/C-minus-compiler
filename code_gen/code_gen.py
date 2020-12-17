from tables import tables
from collections import namedtuple

MidLangDefaults = namedtuple('MidLangDefaults', 'WORD_SIZE DATA_ADDRESS TEMP_ADDRESS')
MID_LANG = MidLangDefaults(4, 500, 1000)


class CodeGen:

    def __init__(self, mid_lang_defaults=MID_LANG):
        self.program_block = []
        self.semantic_stack = []

        self.MLD = mid_lang_defaults
        self.data_address = self.MLD.DATA_ADDRESS
        self.temp_address = self.MLD.TEMP_ADDRESS

        self.routines = {"#pnum": self.pnum,
                         "#pid": self.pid,
                         "#parr": self.parr,
                         "#declare_id": self.declare_id,
                         "#declare_arr": self.declare_arr,
                         "#assign": self.assign,
                         "#op_push": self.op_push,
                         "#op_exec": self.op_exec,
                         "#pop": self.pop,
                         }

    def call(self, routine, token=None):
        try:
            self.routines[routine](token)
            self.export("output.txt")
        except:
            print(f"error during generating code for token {token.lexeme} and routine {routine}")

    def pnum(self, token):
        self.semantic_stack.append(f"#{token.lexeme}")

    def parr(self, token):
        offset = self.semantic_stack.pop()
        temp = self.get_temp_var()
        self.program_block.append(f"(MULT, #4, {offset}, {temp})")
        self.program_block.append(f"(ADD, #{self.semantic_stack.pop()}, {temp}, {temp})")
        self.semantic_stack.append(f"@{temp}")

    def declare_arr(self, token):
        self.get_data_var(int(self.semantic_stack.pop()[1:]) - 1)

    def declare_id(self, token):
        id_record = self.find_var(token.lexeme)
        id_record.address = self.get_data_var()
        self.program_block.append(f"(ASSIGN, #0, {id_record.address}, )")

    def assign(self, token):
        self.program_block.append(f"(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack[-1]}, )")

    def pid(self, token):
        self.semantic_stack.append(self.find_var(token.lexeme).address)

    def op_exec(self, token):
        second = self.semantic_stack.pop()
        operand = self.semantic_stack.pop()
        first = self.semantic_stack.pop()
        result = self.get_temp_var()
        self.program_block.append(f"({operand}, {first}, {second}, {result})")
        self.semantic_stack.append(result)

    operands = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '<': 'LT', '==': 'EQ'}
    def op_push(self, token):
        self.semantic_stack.append(self.operands[token.lexeme])

    def get_temp_var(self):
        self.temp_address += self.MLD.WORD_SIZE
        return self.temp_address - self.MLD.WORD_SIZE

    def get_data_var(self, chunk_size=1):
        self.data_address += self.MLD.WORD_SIZE * chunk_size
        return self.data_address - self.MLD.WORD_SIZE * chunk_size

    def pop(self, token):
        self.semantic_stack.pop()

    @staticmethod
    def find_var(id):
        return tables.get_symbol_table().fetch(id)

    def export(self, path):
        with open(path, "w") as f:
            for i, l in enumerate(self.program_block):
                f.write(f"{i}\t{l}\n")
