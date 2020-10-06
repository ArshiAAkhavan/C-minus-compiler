class TokenMissMatchException(Exception):
    def __init__(self, token_lexeme):
        super(TokenMissMatchException, self).__init__(
            f"could not match lexeme[{token_lexeme}] with any known regular expressions...")


class Edge:
    def __init__(self):
        self.include_ranges = []
        self.exclude_ranges = []

    def include(self, start, end):
        self.include_ranges.append((start, end))
        return self

    def exclude(self, start, end):
        self.exclude_ranges.append((start, end))
        return self

    def __contains__(self,char):
        for start,end in self.exclude_ranges:
            if start<=char and char<=end:
                return False
        
        for start,end in self.include_ranges:
            if char<start or end<char:
                return False
        return True

class DFANode:
    def __init__(self, action=None):
        self.action = action
        self.children = []
    
    def append(self, edge, child):
        self.children.append((edge, child))
        return self

        # for (edge, chDild), _ in self.children:
    def match(self, char):
        for edge,child in self.children:
            if char in edge:
                return child
        return self.action

class Scanner:
    
    def __init__(self,root,input_provider):
        self.root=root
        self.input_provider=input_provider
        self.current_lexeme=""
    
    def get_next_token(self):
        current_state=self.root
        while(self.input_provider.has_next()):
            char=self.input_provider.get_next_char()

            return_value=current_state.match(char)
            if isinstance(return_value,DFANode):
                self.current_lexeme+=char
                current_state=return_value
            else:
                try:
                    return return_value(self.current_lexeme)
                except TypeError:
                    raise TokenMissMatchException(self.current_lexeme)
                finally:
                    self.current_lexeme=""
                    current_state=self.root
        return None

def main():
    from buffer_reader import Buffer_reader
    number_regx=DFANode()
    middle_state=DFANode()
    final_state=DFANode(lambda lexeme: print(f"lexeme is {lexeme}"))
    middle_state.append(Edge().include("0","9"),middle_state).append(Edge().exclude("0","9"),final_state)
    number_regx.append(Edge().include("0","9"),middle_state)

    sc= Scanner(number_regx,Buffer_reader("input.txt",30))
    
    
    while(True):
        try:
            sc.get_next_token()
        except TokenMissMatchException as e:
            print(e)




if __name__=="__main__":
    main()