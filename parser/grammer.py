class Terminal:
    def __init__(self,name):
        self.name=name
        self.first=[name]


class NoneTerminal(Terminal):
    def __init__(self,name , first=[], follow=[]):
        self.name=name
        self.first=first
        self.follow=follow


class Rule:
    def __init__(self,left,right):
        self.left=left
        self.right=right


class Grammer:
    def __init__(self,none_terminals,terminals):
        self.none_terminals=none_terminals
        self.terminals=terminals
        self.rules=[]

    def add_rule(self,rule):
        self.rules.append(rule)

    def import_rules(self,path):
        with open(path) as f: 
            for line in f.readlines():
                raw_rule=line.split("->")
                right=[self.get_element_by_id(e) for e in raw_rule[1].split(" ")]
                left=self.get_element_by_id(raw_rule[0])
                self.add_rule(Rule(left,right))
            
    def import_firsts(self,path):
        with open(path) as f: 
            for line in f.readlines():
                first=line.split(" ")
                nt=self.get_element_by_id(first[0])
                nt.first=[self.get_element_by_id(e) for e in first[1:]]
                
    def import_follows(self,path):
        with open(path) as f: 
            for line in f.readlines():
                follow=line.split(" ")
                nt=self.get_element_by_id(follow[0])
                nt.follow=[self.get_element_by_id(e) for e in follow[1:]]

    def get_element_by_id(self,name):
        for nt in self.none_terminals:
            if nt.name==name: return nt
        for t in self.terminals:
            if t.name==name: return t


def init_terminals():
    terminals = [Terminal('$'), Terminal('ε'), Terminal('ID'), Terminal(';'), Terminal('['), Terminal('NUM'),
                 Terminal(']'), Terminal('('), Terminal(')'), Terminal('int'), Terminal('void'), Terminal(','),
                 Terminal('{'), Terminal('}'), Terminal('break'), Terminal('if'), Terminal('else'), Terminal('while'),
                 Terminal('return'), Terminal('switch'), Terminal('case'), Terminal('default'), Terminal(':'),
                 Terminal('='), Terminal('<'), Terminal('=='), Terminal('+'), Terminal('-'), Terminal('*')]
    return terminals


def init_non_terminals():
    non_terminals = [NoneTerminal('Program'), NoneTerminal('DeclarationList'), NoneTerminal('Declaration'),
                     NoneTerminal('DeclarationInitial'), NoneTerminal('DeclarationPrime'), NoneTerminal('VarDeclarationPrime'),
                     NoneTerminal('FunDeclarationPrime'), NoneTerminal('TypeSpecifier'), NoneTerminal('Params'),
                     NoneTerminal('ParamListVoidAbtar'), NoneTerminal('ParamList'), NoneTerminal('Param'),
                     NoneTerminal('ParamPrime'), NoneTerminal('CompoundStmt'), NoneTerminal('StatementList'),
                     NoneTerminal('Statement'), NoneTerminal('ExpressionStmt'), NoneTerminal('SelectionStmt'),
                     NoneTerminal('IterationStmt'), NoneTerminal('ReturnStmt'), NoneTerminal('ReturnStmtPrime'),
                     NoneTerminal('SwitchStmt'), NoneTerminal('CaseStmts'), NoneTerminal('CaseStmt'),
                     NoneTerminal('DefaultStmt'), NoneTerminal('Expression'), NoneTerminal('B'), NoneTerminal('H'),
                     NoneTerminal('SimpleExpressionZegond'), NoneTerminal('SimpleExpressionPrime'), NoneTerminal('C'),
                     NoneTerminal('Relop'), NoneTerminal('AdditiveExpression'), NoneTerminal('AdditiveExpressionPrime'),
                     NoneTerminal('AdditiveExpressionZegond'), NoneTerminal('D'), NoneTerminal('Addop'), NoneTerminal('Term')
                     , NoneTerminal('TermPrime'), NoneTerminal('TermZegond'), NoneTerminal('G'), NoneTerminal('SignedFactor'),
                     NoneTerminal('SignedFactorPrime'), NoneTerminal('SignedFactorZegond'), NoneTerminal('Factor'),
                     NoneTerminal('VarCallPrime'), NoneTerminal('VarPrime'), NoneTerminal('FactorPrime'),
                     NoneTerminal('FactorZegond'), NoneTerminal('Args'), NoneTerminal('ArgList'), NoneTerminal('ArgListPrime')]
    return non_terminals
