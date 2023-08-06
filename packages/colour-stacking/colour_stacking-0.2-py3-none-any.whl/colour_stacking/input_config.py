from typing import NamedTuple, List


class InputConfig(NamedTuple):
    colour_order: List[str]
    buffer_size: float
    opposite_share_thickness: bool = False
