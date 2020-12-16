class CodeGen:
    def __init__(self):
        self.program_block = []
        self.semantic_stack = []
        self.routines = {"#pnum": self.pnum}

    def call(self, name, token=None):
        self.routines[name](token)

    def pnum(self, token):
        self.semantic_stack.append(f"#{token.lexeme}")
