from enum import Enum, auto


class LexType(Enum):
    object_id = auto()
    func_name = auto()
    add_op = auto()
    sub_op = auto()
    div_op = auto()
    mul_op = auto()
    inc_op = auto()
    dec_op = auto()
    property_op = auto()
    card_op = auto()
    assign_op = auto()
    gamestate_kw = auto()
    reset_kw = auto()
    clear_cards_kw = auto()
    repeat_kw = auto()
    number = auto()
    text = auto()
    left_bracket = auto()
    right_bracket = auto()
    left_curl_bracket = auto()
    right_curl_bracket = auto()
    block_kw = auto()
    attack_kw = auto()
    life_kw = auto()
    remove_kw = auto()
    destroy_kw = auto()
    exile_kw = auto()
    add_kw = auto()
