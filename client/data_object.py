from dataclasses import dataclass, field
from typing import List

import math


@dataclass
class DataObject:

    data_id: int
    multi_control: bool
    value: float

    x: float
    y: float

    rx: float = 0.0
    ry: float = 0.0
    rz: float = 0.0

    width: float = 300.0
    height: float = 300.0

    name: str = ""

    temp_value: float = 0.0

    ctrl_ids: List[int] = field(default_factory=list)

    engaged: bool = False

    rotation: float = 0.0
    previous_rotation: float = 0.0

    translation_x: float = 0.0
    translation_y: float = 0.0

    def set_value(self, value: float):
        self.value = value

    def set_temp_value(self, value: float):
        self.temp_value = value

    def update_location(self, x: float, y: float):
        self.x = x
        self.y = y

    def update_orientation(self, rz: float):
        self.rz = rz

    def add_ctrl_id(self, ctrl_id: int):
        if ctrl_id not in self.ctrl_ids:
            self.ctrl_ids.append(ctrl_id)

    def remove_ctrl_id(self, ctrl_id: int):
        if ctrl_id in self.ctrl_ids:
            self.ctrl_ids.remove(ctrl_id)

    def has_ctrl_id(self, ctrl_id: int) -> bool:
        return ctrl_id in self.ctrl_ids

    def get_ctrl_count(self) -> int:
        return len(self.ctrl_ids)

    def check_hit(self, px: float, py: float) -> bool:

        return (
            abs(self.x - px) < self.width / 2
            and
            abs(self.y - py) < self.height / 2
        )
		