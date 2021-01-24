class Layer:
    def __init__(self, flags):
        self.flags = flags
        self.temp_stack = []
        self.data_stack = []
        self.jail = []

    def new_scope(self):
        self.temp_stack.append(self.flags.temp_address)
        self.data_stack.append(self.flags.data_address)
        self.jail.append("|")

    def del_scope(self):
        self.flags.data_address = self.data_stack.pop()
        self.flags.temp_address = self.temp_stack.pop()

        while self.jail[-1] != "|":  # scope delimiter
            self.prison_break()
        self.jail.pop()

    def prison_break(self):
        break_address = len(self.flags.program_block)
        prisoner = self.jail.pop()
        self.flags.program_block[prisoner] = f"(JP, {break_address}, , )"

    def prison(self):
        self.jail.append(len(self.flags.program_block))
        self.flags.program_block.append("(help me step-programmer im stuck!)")


class ScopeManager:
    def __init__(self, flags, stack):
        self.stack = stack
        self.layers = {"f": Layer(flags), "c": Layer(flags), "i": Layer(flags)}
        self.scmod = []

    def push_scmod(self, mod):
        self.scmod.append(mod)

    def prison(self):
        self.layers[self.scmod.pop()].prison()

    def prison_break(self):
        self.layers[self.scmod.pop()].prison_break()

    def new_scope(self):
        scmod = self.scmod.pop()
        self.layers[scmod].new_scope()
        if scmod == "f":
            self.stack.new_scope()

    def del_scope(self):
        scmod = self.scmod.pop()
        self.layers[scmod].del_scope()
        if scmod == "f":
            self.stack.del_scope()
