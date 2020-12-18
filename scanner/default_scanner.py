from scanner import actions
from scanner.buffer_reader import BufferReader
from scanner.lang import DFANode, FinalStateNode, Edge
from scanner.scanner import Scanner


def number_regex(start):
    # implementing number regex
    num_middle_state = DFANode(actions.error_gen)
    num_final_state = FinalStateNode(actions.num_token_gen, True)
    num_middle_state.append(Edge().include("0", "9"), num_middle_state).append(
        Edge().exclude("0", "9").exclude("a", "z").exclude("A", "Z"), num_final_state)
    start.append(Edge().include("0", "9"), num_middle_state)
    return start


def id_regex(start):
    # implementing id/keyword
    id_middle_state = DFANode(actions.error_gen)
    id_final_state = FinalStateNode(actions.id_token_gen, True)
    id_middle_state.append(Edge().include("0", "9").include("a", "z").include("A", "Z"), id_middle_state) \
        .append(Edge().exclude("0", "9").exclude("a", "z").exclude("A", "Z"), id_final_state)
    start.append(Edge().include("a", "z").include("A", "Z"), id_middle_state)
    return start


def symbol_regex(start):
    # implementing symbols
    symbols_group_final_state = FinalStateNode(
        actions.symbol_token_gen, False)  # 5
    equals_final_state = FinalStateNode(actions.symbol_token_gen, False)  # 7
    assign_middle_state = DFANode(actions.error_gen)  # 6
    star_middle_state = DFANode(actions.error_gen)  # 8
    assign_star_final_state = FinalStateNode(
        actions.symbol_token_gen, True)  # 9
    start.append(Edge().include(":", "<").include(",").include("(", ")").include("[").include("]")
                 .include("{").include("}").include("+").include("-"), symbols_group_final_state)
    start.append(Edge().include("="), assign_middle_state)
    start.append(Edge().include("*"), star_middle_state)
    assign_middle_state.append(Edge().include("="), equals_final_state).append(
        Edge().exclude("="), assign_star_final_state)
    star_middle_state.append(Edge().exclude("/"), assign_star_final_state)
    return start


def comment_regex(start):
    # implementing comments
    comment_start_state = DFANode(actions.error_gen, supports_all_langs=True)  # a
    a_error = FinalStateNode(actions.error_gen, push_back_mode=True, supports_all_langs=True)  # as a has no other
    short_comment_middle_state = DFANode(actions.error_gen, supports_all_langs=True)  # b
    comment_final_state = FinalStateNode(actions.comment_token_gen, push_back_mode=False,
                                         supports_all_langs=True)  # c
    long_comment_start_state = DFANode(actions.error_gen, supports_all_langs=True)  # d
    long_comment_end_state = DFANode(actions.error_gen, supports_all_langs=True)  # e
    start.append(Edge().include("/"), comment_start_state)
    comment_start_state.append(Edge().include("/"), short_comment_middle_state) \
        .append(Edge().include("*"), long_comment_start_state).append(Edge().exclude('/').exclude('*'), a_error)
    short_comment_middle_state.append(Edge().include('\n'), comment_final_state).append(
        Edge().exclude('\n'), short_comment_middle_state)
    long_comment_start_state.append(Edge().include("*"), long_comment_end_state).append(Edge().exclude("*")
                                                                                        .exclude(chr(26)),
                                                                                        long_comment_start_state)
    long_comment_end_state.append(Edge().exclude("*").exclude("/").exclude(chr(26)), long_comment_start_state) \
        .append(Edge().include("*"), long_comment_end_state).append(Edge().include("/"), comment_final_state)
    return start


def whitespace_regex(start):
    # implementing whitespace
    whitespace_final_state = FinalStateNode(
        actions.whitespace_token_gen, False)
    start.append(Edge().include('\t', '\r').include(' ').include(chr(26)), whitespace_final_state)
    return start


def build_scanner(path):
    start = DFANode(actions.error_gen)
    number_regex(start)
    id_regex(start)
    symbol_regex(start)
    comment_regex(start)
    whitespace_regex(start)

    language = Edge().include('0', '9').include('a', 'z').include('A', 'Z') \
        .include('/').include('*') \
        .include(':', '<').include(',').include('(', ')').include('[').include(']').include('{').include('}') \
        .include('+').include('-').include('=') \
        .include('\t', '\r').include(' ').include(chr(26))
    return Scanner(start, BufferReader(path, 30), language)


