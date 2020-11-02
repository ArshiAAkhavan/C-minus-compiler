class Terminal:
    def __init__(self, name):
        self.name = name
        self.first = [name]

    def __str__(self):
        s = f"{self.name}"
        return s


class NonTerminal(Terminal):
    def __init__(self, name, first=[], follow=[]):
        self.name = name
        self.first = first
        self.follow = follow

    def __str__(self):
        s = f"{self.name}"
        return s


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Grammar:
    def __init__(self, non_terminals, terminals):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = []
        self.predict_sets = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def import_rules(self, path):
        with open(path, encoding='utf-8') as f:
            for line in f.readlines():
                raw_rule = line.split("->")
                raw_rule[1].strip('\n')
                right = []
                for e in raw_rule[1].split(" "):
                    if e:
                        right.append(self.get_element_by_id(e.rstrip()))
                left = self.get_element_by_id(raw_rule[0].rstrip())
                self.add_rule(Rule(left, right))

    def import_firsts(self, path):
        with open(path, encoding='utf-8') as f:
            for line in f.readlines():
                first = line.split(" ")
                nt = self.get_element_by_id(first[0])
                nt.first = [self.get_element_by_id(e.rstrip()) for e in first[1:]]

    def import_follows(self, path):
        with open(path) as f:
            for line in f.readlines():
                follow = line.split(" ")
                nt = self.get_element_by_id(follow[0])
                nt.follow = [self.get_element_by_id(e.rstrip()) for e in follow[1:]]

    def import_predict_sets(self, path):
        with open(path) as f:
            for line in f.readlines():
                predict_set = line.split(" ")
                self.predict_sets.append([self.get_element_by_id(e.rstrip()) for e in predict_set[0:]])

    def get_element_by_id(self, name):
        for nt in self.non_terminals:
            if nt.name == name: return nt
        for t in self.terminals:
            if t.name == name: return t


def init_terminals():
    terminals = [Terminal('$'), Terminal('ε'), Terminal('ID'), Terminal(';'), Terminal('['), Terminal('NUM'),
                 Terminal(']'), Terminal('('), Terminal(')'), Terminal('int'), Terminal('void'), Terminal(','),
                 Terminal('{'), Terminal('}'), Terminal('break'), Terminal('if'), Terminal('else'), Terminal('while'),
                 Terminal('return'), Terminal('switch'), Terminal('case'), Terminal('default'), Terminal(':'),
                 Terminal('='), Terminal('<'), Terminal('=='), Terminal('+'), Terminal('-'), Terminal('*')]
    return terminals


def init_non_terminals():
    non_terminals = [NonTerminal('Program'), NonTerminal('DeclarationList'), NonTerminal('Declaration'),
                     NonTerminal('DeclarationInitial'), NonTerminal('DeclarationPrime'),
                     NonTerminal('VarDeclarationPrime'),
                     NonTerminal('FunDeclarationPrime'), NonTerminal('TypeSpecifier'), NonTerminal('Params'),
                     NonTerminal('ParamListVoidAbtar'), NonTerminal('ParamList'), NonTerminal('Param'),
                     NonTerminal('ParamPrime'), NonTerminal('CompoundStmt'), NonTerminal('StatementList'),
                     NonTerminal('Statement'), NonTerminal('ExpressionStmt'), NonTerminal('SelectionStmt'),
                     NonTerminal('IterationStmt'), NonTerminal('ReturnStmt'), NonTerminal('ReturnStmtPrime'),
                     NonTerminal('SwitchStmt'), NonTerminal('CaseStmts'), NonTerminal('CaseStmt'),
                     NonTerminal('DefaultStmt'), NonTerminal('Expression'), NonTerminal('B'), NonTerminal('H'),
                     NonTerminal('SimpleExpressionZegond'), NonTerminal('SimpleExpressionPrime'), NonTerminal('C'),
                     NonTerminal('Relop'), NonTerminal('AdditiveExpression'), NonTerminal('AdditiveExpressionPrime'),
                     NonTerminal('AdditiveExpressionZegond'), NonTerminal('D'), NonTerminal('Addop'),
                     NonTerminal('Term'), NonTerminal('TermPrime'), NonTerminal('TermZegond'), NonTerminal('G'),
                     NonTerminal('SignedFactor'), NonTerminal('SignedFactorPrime'), NonTerminal('SignedFactorZegond'),
                     NonTerminal('Factor'), NonTerminal('VarCallPrime'), NonTerminal('VarPrime'),
                     NonTerminal('FactorPrime'), NonTerminal('FactorZegond'), NonTerminal('Args'),
                     NonTerminal('ArgList'), NonTerminal('ArgListPrime')]
    return non_terminals


def init_grammar():
    grammar = Grammar(init_non_terminals(), init_terminals())
    grammar.import_firsts("Firsts.csv")
    grammar.import_follows("Follows.csv")
    grammar.import_rules("grammer.txt")
    grammar.import_predict_sets("Predicts.csv")
    return grammar


if __name__ == "__main__":
    g = init_grammar()
