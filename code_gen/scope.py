class Layer:
    def __init__(self, assembler):
        self.assembler = assembler
        self.temp_stack = []
        self.data_stack = []
        self.jail = []

    def new_scope(self):
        self.temp_stack.append(self.assembler.temp_address)
        self.data_stack.append(self.assembler.data_address)
        self.jail.append("|")

    def del_scope(self):
        self.assembler.data_address = self.data_stack.pop()
        self.assembler.temp_address = self.temp_stack.pop()

        while self.jail[-1] != "|":  # scope delimiter
            self.prison_break()
        self.jail.pop()

    def prison_break(self):
        break_address = len(self.assembler.program_block)
        prisoner = self.jail.pop()
        self.assembler.program_block[prisoner] = f"(JP, {break_address}, , )"

    def prison(self):
        self.jail.append(len(self.assembler.program_block))
        self.assembler.program_block.append("(help step-programmer im stuck!)")


class ScopeManager:
    def __init__(self, assembler, stack):
        self.should_delete_scope = False
        self.stack = stack
        self.layers = {"t": Layer(assembler), "f": Layer(assembler), "c": Layer(assembler), "s": Layer(assembler)}
        self.scmod = []

    def push_scmod(self, mod):
        self.scmod.append(mod)
        if self.should_delete_scope:
            self.__del_scope()

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
        self.should_delete_scope = True

    def __del_scope(self):
        self.should_delete_scope = False
        scmod = self.scmod.pop()
        self.layers[scmod].del_scope()
        if scmod == "f":
            self.stack.del_scope()
