class CodeGen:
    def __init__(self):
        self.routines = {"#pnum": self.pnum}

    def call(self, name):
        self.routines[name]()

    def pnum(self):
        print("num")
