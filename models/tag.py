import time
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np


@dataclass
class Tag:

    tag_id: int

    ttl: int = 200

    active: bool = False

    timestamp: float = 0.0

    tx: float = 0.0
    ty: float = 0.0
    tz: float = 0.0

    rx: float = 0.0
    ry: float = 0.0
    rz: float = 0.0

    corners: Optional[List[np.ndarray]] = field(default_factory=list)

    def check_active(self):

        now = time.time() * 1000

        if self.active and (now - self.timestamp) > self.ttl:

            self.active = False

            from api import tag_absent_3d

            tag_absent_3d(
                self.tag_id,
                self.tx,
                self.ty,
                self.tz,
                self.rx,
                self.ry,
                self.rz
            )

    def set(
        self,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz,
        corners
    ):

        self.timestamp = time.time() * 1000

        self.tx = tx
        self.ty = ty
        self.tz = tz

        self.rx = rx
        self.ry = ry
        self.rz = rz

        self.corners = corners

        from api import (
            tag_present_3d,
            tag_update_3d
        )

        if not self.active:

            tag_present_3d(
                self.tag_id,
                tx,
                ty,
                tz,
                rx,
                ry,
                rz
            )

        else:

            tag_update_3d(
                self.tag_id,
                tx,
                ty,
                tz,
                rx,
                ry,
                rz
            )

        self.active = True
		