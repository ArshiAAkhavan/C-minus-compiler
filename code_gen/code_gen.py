import sys

from tables import tables
from collections import namedtuple
from code_gen.register import RegisterFile
from code_gen.flags import Flag
from code_gen.stack import StackManager

MidLangDefaults = namedtuple('MidLangDefaults', 'WORD_SIZE DATA_ADDRESS STACK_ADDRESS TEMP_ADDRESS')
MID_LANG = MidLangDefaults(4, 500, 700, 1000)


class CodeGen:

    def __init__(self, mid_lang_defaults=MID_LANG):
        self.program_block = []
        self.semantic_stack = []
        self.jail = []

        self.MLD = mid_lang_defaults
        self.data_address = self.MLD.DATA_ADDRESS
        self.stack_address = self.MLD.STACK_ADDRESS
        self.temp_address = self.MLD.TEMP_ADDRESS

        self.flags = Flag()
        self.rf = RegisterFile(self.get_data_var(), self.get_data_var(), self.get_data_var(), self.get_data_var())
        self.stack = StackManager(self.program_block, self.rf, self.MLD)

        self.apply_template()

        self.routines = {"#pnum": self.pnum,
                         "#pid": self.pid,
                         "#parr": self.parr,
                         "#pzero": self.pzero,
                         "#prv": self.prv,
                         "#op_push": self.op_push,
                         "#pop": self.pop,

                         "#declare_id": self.declare_id,
                         "#declare_arr": self.declare_arr,
                         "#declare_func": self.declare_func,

                         "#arg_init": self.arg_init,
                         "#arg_finish": self.arg_finish,
                         "#arg_pass": self.arg_pass,

                         "#assign": self.assign,
                         "#op_exec": self.op_exec,
                         "#decide": self.decide,
                         "#case": self.case,

                         "#hold": self.hold,
                         "#label": self.label,

                         "#prison_break": self.prison_break,
                         "#prison": self.prison,
                         "#jump_while": self.jump_while,

                         "#output": self.output,
                         "#call": self.func_call,
                         "#return": self.func_return,

                         "#sc_start": self.scope_start,
                         "#sc_stop": self.scope_stop,
                         }

    def call(self, routine, token=None):
        try:
            if routine == "#call":
                print("ali")
            self.routines[routine](token)
            # uncomment the line below for debugging , gives you a step by step view!
            self.export("output.txt")
        except:
            sys.stderr.write(f"error during generating code for token {token.lexeme} and routine {routine}\n")

    def pid(self, token):
        self.semantic_stack.append(self.find_var(token.lexeme).address)

    def pnum(self, token):
        self.semantic_stack.append(f"#{token.lexeme}")

    def pzero(self, token=None):
        self.semantic_stack.append(f"#0")

    def prv(self, token=None):
        self.semantic_stack.append(self.rf.rv)

    def parr(self, token=None):
        offset = self.semantic_stack.pop()
        temp = self.get_temp_var()
        self.program_block.append(f"(MULT, #{self.MLD.WORD_SIZE}, {offset}, {temp})")
        self.program_block.append(f"(ADD, {self.semantic_stack.pop()}, {temp}, {temp})")
        self.semantic_stack.append(f"@{temp}")

    def pop(self, token=None):
        self.semantic_stack.pop()

    def declare_arr(self, token=None):
        self.program_block.append(f"(ASSIGN, {self.rf.sp}, {self.semantic_stack[-2]}, )")
        self.stack.reserve(int(self.semantic_stack.pop()[1:]))

    def declare_func(self, token=None):
        self.flags.data_pointer = self.data_address
        self.flags.temp_pointer = self.temp_address
        self.program_block.append(f"(ASSIGN, #{len(self.program_block) + 1}, {self.semantic_stack[-1]}, )")

    def declare_id(self, token):
        id_record = self.find_var(token.lexeme)
        id_record.address = self.get_data_var()

        if self.flags.arg_dec:
            self.arg_assign(id_record.address)

        # uncomment the line below for debugging
        # self.program_block.append(f"(ASSIGN, #0, {id_record.address}, )")

    def assign(self, token=None):
        self.program_block.append(f"(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack[-1]}, )")

    def op_exec(self, token=None):
        second = self.semantic_stack.pop()
        operand = self.semantic_stack.pop()
        first = self.semantic_stack.pop()
        result = self.get_temp_var()
        self.program_block.append(f"({operand}, {first}, {second}, {result})")
        self.semantic_stack.append(result)

    operands = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '<': 'LT', '==': 'EQ'}

    def op_push(self, token):
        self.semantic_stack.append(self.operands[token.lexeme])

    def hold(self, token=None):
        self.label()
        self.program_block.append("(new you see me!)")

    def label(self, token=None):
        self.semantic_stack.append(len(self.program_block))

    def prison(self, token=None):
        self.jail.append(len(self.program_block))
        self.program_block.append("(help me step-programmer im stuck!)")

    def prison_break(self, token=None):
        break_address = len(self.program_block)
        prisoner = self.jail.pop()
        self.program_block[prisoner] = f"(JP, {break_address}, , )"

    def scope_start(self, token=None):
        tables.get_symbol_table().new_scope()
        self.jail.append("|")  # scope delimiter
        self.stack.new_scope()

    def scope_stop(self, token=None):
        tables.get_symbol_table().remove_scope()

        while self.jail[-1] != "|":  # scope delimiter
            self.prison_break()
        self.jail.pop()
        self.stack.del_scope()

    def decide(self, token=None):
        address = self.semantic_stack.pop()
        self.program_block[address] = f"(JPF, {self.semantic_stack.pop()}, {len(self.program_block)}, )"

    def case(self, token=None):
        result = self.get_temp_var()
        self.program_block.append(f"(EQ, {self.semantic_stack.pop()}, {self.semantic_stack[-1]}, {result})")
        self.semantic_stack.append(result)

    def jump_while(self, token=None):
        head1 = self.semantic_stack.pop()
        head2 = self.semantic_stack.pop()
        self.program_block.append(f"(JP, {self.semantic_stack.pop()}, , )")
        self.semantic_stack.append(head2)
        self.semantic_stack.append(head1)

        # passing arguments

    def output(self, token=None):
        self.program_block.append(f"(PRINT, {self.semantic_stack.pop()}, , )")

    def get_temp_var(self):
        self.temp_address += self.MLD.WORD_SIZE
        return self.temp_address - self.MLD.WORD_SIZE

    def get_data_var(self, chunk_size=1):
        self.data_address += self.MLD.WORD_SIZE * chunk_size
        return self.data_address - self.MLD.WORD_SIZE * chunk_size

    def func_call(self, token=None):
        # storing data
        for data in range(self.flags.data_pointer, self.data_address, self.MLD.WORD_SIZE):
            self.stack.push(data)
        # storing temp
        for temp in range(self.flags.temp_pointer, self.temp_address, self.MLD.WORD_SIZE):
            self.stack.push(temp)
        # storing registers
        self.stack.store_registers()
        # arg pass
        for arg in range(self.flags.arg_pass, len(self.semantic_stack)):
            self.stack.push(self.semantic_stack[arg])
        for arg in range(self.flags.arg_pass, len(self.semantic_stack)):
            self.semantic_stack.pop()
        # setting registers
        self.program_block.append(f"(ASSIGN, #{len(self.program_block) + 2}, {self.rf.ra}, )")
        # call!
        self.program_block.append(f"(JP, @{self.semantic_stack.pop()}, , )")
        # collect
        self.semantic_stack.append(self.rf.rv)

        # !!!gnihtyreve gnitrever
        # loading registers
        self.stack.load_registers()
        # loading temps
        for temp in range(self.temp_address, self.flags.temp_pointer, -self.MLD.WORD_SIZE):
            self.stack.pop(temp - self.MLD.WORD_SIZE)
        # loading temps
        for data in range(self.data_address, self.flags.data_pointer, -self.MLD.WORD_SIZE):
            self.stack.pop(data - self.MLD.WORD_SIZE)

    def func_return(self, token=None):
        self.program_block.append(f"(JP, @{self.rf.ra}, )")

    # argument management
    def arg_init(self, token=None):
        self.flags.arg_dec = True

    def arg_finish(self, token=None):
        self.flags.arg_dec = False

    def arg_assign(self, address):
        self.stack.pop(address)

    def arg_pass(self, token=None):
        self.flags.arg_pass = len(self.semantic_stack)

    @staticmethod
    def find_var(id):
        return tables.get_symbol_table().fetch(id)

    def export(self, path):
        with open(path, "w") as f:
            for i, l in enumerate(self.program_block):
                f.write(f"{i}\t{l}\n")

    def apply_template(self):
        self.program_block.append(f"(ASSIGN, #{self.MLD.STACK_ADDRESS}, {self.rf.sp}, )")
        self.program_block.append(f"(ASSIGN, #{self.MLD.STACK_ADDRESS}, {self.rf.fp}, )")
        self.hold()

    def patch(self):
        id_record = self.find_var("main")
        self.program_block[self.semantic_stack.pop()] = f"(JP, {id_record.address}, , )"
