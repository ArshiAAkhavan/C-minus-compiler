class StackManager:
    def __init__(self, program_block, register_file, MLD):
        self.MLD = MLD
        self.program_block = program_block
        self.rf = register_file

    # stack management
    def push(self, value):
        self.program_block.append(f"(ASSIGN, {value}, @{self.rf.sp}, )")
        self.program_block.append(f"(ADD, {self.rf.sp}, #{self.MLD.WORD_SIZE}, {self.rf.sp})")
        # self.debug()

    def pop(self, holder):
        # self.debug()
        self.program_block.append(f"(SUB, {self.rf.sp}, #{self.MLD.WORD_SIZE}, {self.rf.sp})")
        # self.debug()
        self.program_block.append(f"(ASSIGN, @{self.rf.sp}, {holder}, )")
        # self.debug()

    def new_scope(self):
        self.push(self.rf.fp)
        self.program_block.append(f"(ASSIGN, {self.rf.sp}, {self.rf.fp}, )")
        # self.debug()

    def del_scope(self):
        self.program_block.append(f"(ASSIGN, {self.rf.fp}, {self.rf.sp}, )")
        self.pop(self.rf.fp)
        # self.debug()

    def reserve(self, chunk=1):
        self.program_block.append(f"(ADD, #{self.MLD.WORD_SIZE * chunk}, {self.rf.sp}, {self.rf.sp})")

    def debug(self):
        self.program_block.append(f"(PRINT, 500, , )")
        self.program_block.append(f"(PRINT, 504, , )")
        # todo remove debug
        # pass
