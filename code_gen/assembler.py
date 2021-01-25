class Assembler:
    def __init__(self):
        self.arg_dec = False
        self.set_exec = False
        self.arg_pointer = []
        self.data_pointer = 0
        self.temp_pointer = 0
        self.last_id = None
        self.temp_address = 0
        self.data_address = 0
        self.stack_address = 0
        self.program_block = []
