class StackManager:
    def __init__(self, program_block, register_file, MLD):
        self.MLD = MLD
        self.program_block = program_block
        self.rf = register_file

    # stack management
    def push(self, value):
        self.program_block.append(f"(ASSIGN, {value}, @{self.rf.sp}, )")
        self.program_block.append(f"(ADD, #4, {self.rf.sp}, {self.rf.sp})")

    def pop(self, holder):
        self.program_block.append(f"(SUB, #4, {self.rf.sp}, {self.rf.sp})")
        self.program_block.append(f"(ASSIGN, @{self.rf.sp}, {holder}, )")

    def new_scope(self):
        self.push(self.rf.fp)
        self.program_block.append(f"(ASSIGN, {self.rf.sp}, {self.rf.fp}, )")

    def del_scope(self):
        self.program_block.append(f"(ASSIGN, {self.rf.fp}, {self.rf.sp}, )")
        self.pop(self.rf.fp)

    def reserve(self, chunk=1):
        self.program_block.append(f"(ADD, #{self.MLD.WORD_SIZE * chunk}, {self.rf.sp}, {self.rf.sp})")

