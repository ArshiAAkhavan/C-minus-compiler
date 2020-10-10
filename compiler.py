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

start = DFANode(actions.error_gen)
number_regex(start)
id_regex(start)
symbol_regex(start)


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
print(tables.get_token_table())
tables.get_error_table().end()
tables.get_symbol_table().end()


