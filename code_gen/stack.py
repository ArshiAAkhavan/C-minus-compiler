class StackManager:
    def __init__(self, program_block, register_file, MLD):
        self.MLD = MLD
        self.program_block = program_block
        self.rf = register_file

    def push(self, value):
        self.program_block.append(f"(ASSIGN, {value}, @{self.rf.sp}, )")
        self.program_block.append(f"(ADD, {self.rf.sp}, #{self.MLD.WORD_SIZE}, {self.rf.sp})")

    def pop(self, holder):
        self.program_block.append(f"(SUB, {self.rf.sp}, #{self.MLD.WORD_SIZE}, {self.rf.sp})")
        self.program_block.append(f"(ASSIGN, @{self.rf.sp}, {holder}, )")

    def new_scope(self):
        self.program_block.append("")
        self.push(self.rf.fp)
        self.program_block.append(f"(ASSIGN, {self.rf.sp}, {self.rf.fp}, )")

    def del_scope(self):
        self.program_block.append(f"(ASSIGN, {self.rf.fp}, {self.rf.sp}, )")
        self.pop(self.rf.fp)
        self.program_block.append("")

    def reserve(self, chunk=1):
        self.program_block.append(f"(ADD, #{self.MLD.WORD_SIZE * chunk}, {self.rf.sp}, {self.rf.sp})")

    def debug(self):
        self.program_block.append(f"(PRINT, 500, , )")
        self.program_block.append(f"(PRINT, 504, , )")

    def store_registers(self):
        self.push(self.rf.sp)
        self.push(self.rf.fp)
        self.push(self.rf.ra)

    def load_registers(self):
        self.pop(self.rf.ra)
        self.pop(self.rf.fp)
        self.pop(self.rf.sp)
