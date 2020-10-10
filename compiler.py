from buffer_reader import BufferReader
from scanner import *


def number_regex(start):
    # implementing number regex
    num_middle_state = DFANode(actions.error_gen)
    num_final_state = FinalStateNode(actions.num_token_gen, True)
    num_middle_state.append(Edge().include("0", "9"), num_middle_state).append(Edge().exclude("0", "9").exclude("a","z").exclude("A","Z"), num_final_state)
    start.append(Edge().include("0", "9"), num_middle_state)

def id_regex(start):
    # implementing id/keyword
    id_middle_state = DFANode(actions.error_gen)
    id_final_state = FinalStateNode(actions.id_token_gen, True)
    id_middle_state.append(Edge().include("0", "9").include("a", "z").include("A", "Z"), id_middle_state)\
        .append(Edge().exclude("0", "9").exclude("a", "z").exclude("A", "Z"), id_final_state)
    start.append(Edge().include("a", "z").include("A", "Z"), id_middle_state)

def symbol_regex(start):
    # implementing symbols
    symbols_group_final_state = FinalStateNode(actions.symbol_token_gen, False) # 5
    equals_final_state = FinalStateNode(actions.symbol_token_gen, False) # 7
    assign_middle_state = DFANode(actions.error_gen) # 6
    star_middle_state = DFANode(actions.error_gen) # 8
    assign_star_final_state = FinalStateNode(actions.symbol_token_gen, True) # 9
    start.append(Edge().include(":", "<").include(",", ",").include("(", ")").include("[", "[").include("]", "]")
                    .include("{", "{").include("}", "}").include("+", "+").include("-", "-"), symbols_group_final_state)
    start.append(Edge().include("=", "="), assign_middle_state)
    start.append(Edge().include("*", "*"), star_middle_state)
    assign_middle_state.append(Edge().include("=", "="), equals_final_state).append(Edge().exclude("=", "="), assign_star_final_state)
    star_middle_state.append(Edge().exclude("/", "/"), assign_star_final_state)

def comment_regex(start):
    # implementing comments
    comment_start_state = DFANode(actions.error_gen) # a
    short_comment_middle_state = DFANode(actions.error_gen) # b
    comment_final_state = FinalStateNode(actions.comment_token_gen, False) # c
    long_comment_start_state = DFANode(actions.error_gen) # d
    long_comment_end_state = DFANode(actions.error_gen) # e
    start.append(Edge().include("/", "/"), comment_start_state)
    comment_start_state.append(Edge().include("/", "/"), short_comment_middle_state).append(Edge().include("*", "*"),
                                                                                            long_comment_start_state)
    short_comment_middle_state.append(Edge().include('\n', '\n'), comment_final_state).append(Edge().exclude('\n', '\n')
                                                                                        , short_comment_middle_state)
    long_comment_start_state.append(Edge().include("*", "*"), long_comment_end_state).append(Edge().exclude("*", "*")
                                                                                             .exclude(chr(26), chr(26))
                                                                                             , long_comment_start_state)
    long_comment_end_state.append(Edge().exclude("*", "*").exclude("/", "/"), long_comment_start_state)\
        .append(Edge().include("*", "*"), long_comment_end_state).append(Edge().include("/", "/"), comment_final_state)

def whitespace_regex(start):
    # implementing whitespace
    whitespace_final_state = FinalStateNode(actions.whitespace_token_gen, False)
    start.append(Edge().include('\t', '\r').include(' ', ' ').include(chr(26), chr(26)), whitespace_final_state)


start = DFANode(actions.error_gen)
number_regex(start)
id_regex(start)
symbol_regex(start)
comment_regex(start)
whitespace_regex(start)

sc = Scanner(start, BufferReader("input.txt", 30))

while(sc.can_generate_token()):
    try:
        sc.get_next_token()
    except TokenMissMatchException as e:
        print(e)
    except NotEnoughCharacterException as e:
        print(e)
        break

import tables
tables.get_error_table().export("lexical_errors.txt")
tables.get_symbol_table().export("symbol_table.txt")
tables.get_token_table().export("tokens.txt")
print(tables.get_token_table())


