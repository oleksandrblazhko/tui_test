from dataclasses import dataclass, field
import time

from tools import PVector


@dataclass
class Tag:

    id: int

    TTL: int = 200

    active: bool = False

    ts: int = 0

    tx: float = 0.0
    ty: float = 0.0
    tz: float = 0.0

    rx: float = 0.0
    ry: float = 0.0
    rz: float = 0.0

    corners: list = field(
        default_factory=lambda: [
            PVector(),
            PVector(),
            PVector(),
            PVector()
        ]
    )

    def millis(self):
        return int(time.time() * 1000)

    def check_active(self):

        if (
            self.active
            and
            (self.millis() - self.ts) > self.TTL
        ):

            self.active = False

            from api import tag_absent_3d

            tag_absent_3d(
                self.id,
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

        self.ts = self.millis()

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
                self.id,
                self.tx,
                self.ty,
                self.tz,
                self.rx,
                self.ry,
                self.rz
            )

        else:

            tag_update_3d(
                self.id,
                self.tx,
                self.ty,
                self.tz,
                self.rx,
                self.ry,
                self.rz
            )

        self.active = True

    # Processing aliases

    checkActive = check_active
    
    