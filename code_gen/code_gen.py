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
                         "#declare_id": self.declare_id,
                         "#assign": self.assign,
                         "#mul": self.mul,
                         "#add": self.add,
                         "#sub": self.sub,
                         }

    def call(self, name, token=None):
        self.routines[name](token)

    def pnum(self, token):
        self.semantic_stack.append(f"#{token.lexeme}")

    def declare_id(self, token):
        id_record = self.find_var(token.lexeme)
        id_record.address = self.get_data_var()
        self.program_block.append(f"(ASSIGN, #0, {id_record.address}, )")

    def assign(self, token):
        self.program_block.append(f"(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack.pop()}, )")

    def pid(self, token):
        self.semantic_stack.append(self.find_var(token.lexeme).address)

    def __operation(self, operand):
        result = self.get_temp_var()
        self.program_block.append(f"({operand}, {self.semantic_stack.pop()}, {self.semantic_stack.pop()}, {result})")
        self.semantic_stack.append(result)

    def mul(self, token):
        self.__operation("MULT")

    def add(self, token):
        self.__operation("ADD")

    def sub(self, token):
        self.__operation("SUB")

    def get_temp_var(self):
        self.temp_address += self.MLD.WORD_SIZE
        return self.temp_address - self.MLD.WORD_SIZE

    def get_data_var(self):
        self.data_address += self.MLD.WORD_SIZE
        return self.data_address - self.MLD.WORD_SIZE

    @staticmethod
    def find_var(id):
        return tables.get_symbol_table().fetch(id)

    def export(self, path):
        with open(path, "w") as f:
            for i, l in enumerate(self.program_block):
                f.write(f"{i}\t{l}\n")
