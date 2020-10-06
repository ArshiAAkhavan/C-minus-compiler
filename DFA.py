class TokenMissMatchException(Exception):
    def __init__(self, token_lexeme):
        super(TokenMissMatchException, self).__init__(f"could not match lexeme[{token_lexeme}] with any known regular expressions...")

class Node:
    def __init__(self,action=None):
        self.action=action
        self.children=[]
        self.current_token=""
    
    def append(self,edge,child):
        self.children.append((edge,child))
    
    def match(self,char):
        for (edge,child),_ in self.children:
            if char in edge:
                return child
        try:
            return self.action(self.current_token)
        except TypeError:
            raise TokenMissMatchException
class DFA:
    pass