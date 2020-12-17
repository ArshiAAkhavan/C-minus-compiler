from tables import tables


class CodeGen:
    def __init__(self, data_address=100, temp_address=500):
        self.program_block = []
        self.semantic_stack = []
        self.data_address = data_address
        self.temp_address = temp_address
        self.routines = {"#pnum":       self.pnum,
                         "#pid":        self.pid,
                         "#declare_id": self.declare_id,
                         "#assign": self.assign,
                         }

    def call(self, name, token=None):
        self.routines[name](token)

    def pnum(self, token):
        self.semantic_stack.append(f"#{token.lexeme}")

    def declare_id(self, token):
        id_record = self.find_var(token.lexeme)
        id_record.address = self.get_temp_var()
        self.program_block.append(f"(ASSIGN, #0, {id_record.address}, )")

    def assign(self, token):
        self.program_block.append(f"(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack.pop()}, )")

    def pid(self, token):
        self.semantic_stack.append(self.find_var(token.lexeme).address)

    def get_temp_var(self):
        self.temp_address += 4
        return self.temp_address - 4

    @staticmethod
    def find_var(id):
        return tables.get_symbol_table().fetch(id)

    def export(self, path):
        with open(path, "w") as f:
            for i,l in enumerate(self.program_block):
                f.write(f"{i}\t{l}\n")
