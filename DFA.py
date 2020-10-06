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

    def exclude(self, start, end):
        self.exclude_ranges.append((start, end))

    def __contains__(self,char):
        for (start,end),_ in self.exclude_ranges:
            if start<=char and char<=end:
                return False
        
        for (start,end),_ in self.include_ranges:
            if char<start or end<char:
                return False
        return True

class DFANode:
    def __init__(self, action=None):
        self.action = action
        self.children = []
    
    def append(self, edge, child):
        self.children.append((edge, child))

    def match(self, char):
        for (edge, child), _ in self.children:
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
                    return_value(self.current_lexeme)
                except TypeError:
                    raise TokenMissMatchException
                finally:
                    self.current_lexeme=""
                    current_state=self.root

