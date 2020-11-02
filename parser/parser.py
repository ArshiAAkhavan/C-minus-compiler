class LL1:
    def __init__(self,token_generator,grammer):
        self.token_generator=token_generator
        self.grammer=grammer
        self.p_table=[]
        self.create_parse_table()

    def create_parse_table(self):
        for nt in self.grammer.none_terminals:
