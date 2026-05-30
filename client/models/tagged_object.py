# models/tagged_object.py

import math
import time

from tools import (
    PVector,
    planePoints,
    touchThreshold,
    distance_point_to_plane,
    transform_point,
    img2screen,
)


class TaggedObject:

    def __init__(self, to_ids, offsets):

        self.TTL = 100

        self.active = False
        self.ts = 0

        self.ids = list(to_ids)
        self.offs = list(offsets)

        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0

        self.rx = 0.0
        self.ry = 0.0
        self.rz = 0.0

        self.p_rx = 0.0
        self.p_ry = 0.0
        self.p_rz = 0.0

    # --------------------------------------------------
    # Processing: getTO_ID()
    # --------------------------------------------------

    def get_to_id(self):

        return self.ids[0]

    # --------------------------------------------------
    # Processing: unwrapAngle()
    # --------------------------------------------------

    def unwrap_angle(
        self,
        current_angle,
        previous_angle
    ):

        delta_angle = current_angle - previous_angle

        if delta_angle > math.pi:
            current_angle -= 2.0 * math.pi

        elif delta_angle < -math.pi:
            current_angle += 2.0 * math.pi

        return current_angle

    # --------------------------------------------------
    # Processing: setInactive()
    # --------------------------------------------------

    def set_inactive(self):

        now = int(time.time() * 1000)

        if self.active and (now - self.ts) > self.TTL:

            self.active = False

            try:
                from api import to_absent_2d

                to_absent_2d(
                    self.get_to_id(),
                    self.tx,
                    self.ty,
                    self.tz,
                    self.rz
                )
            except Exception:
                pass

    # --------------------------------------------------
    # Processing: set(...)
    # --------------------------------------------------

    def set(
        self,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz
    ):

        self.tx = tx
        self.ty = ty
        self.tz = tz

        self.rx = self.unwrap_angle(rx, self.p_rx)
        self.ry = self.unwrap_angle(ry, self.p_ry)
        self.rz = self.unwrap_angle(rz, self.p_rz)

        distance = distance_point_to_plane(
            PVector(tx, ty, tz),
            planePoints
        )

        now = int(time.time() * 1000)

        if distance < touchThreshold:

            try:
                from api import (
                    to_present_2d,
                    to_update_2d
                )

                if not self.active:

                    to_present_2d(
                        self.get_to_id(),
                        self.tx,
                        self.ty,
                        self.tz,
                        self.rz
                    )

                else:

                    to_update_2d(
                        self.get_to_id(),
                        self.tx,
                        self.ty,
                        self.tz,
                        self.rz
                    )

            except Exception:
                pass

            self.active = True
            self.ts = now

        else:

            if self.active and (now - self.ts) > self.TTL:

                self.active = False

                try:
                    from api import to_absent_2d

                    to_absent_2d(
                        self.get_to_id(),
                        self.tx,
                        self.ty,
                        self.tz,
                        self.rz
                    )
                except Exception:
                    pass

        # Processing-аналог p_rx/p_ry/p_rz
        self.p_rx = self.rx
        self.p_ry = self.ry
        self.p_rz = self.rz

    # --------------------------------------------------
    # Processing: getScreenLoc2D()
    # --------------------------------------------------

    def get_screen_loc_2d(
        self,
        homography
    ):

        point = transform_point(
            PVector(
                self.tx,
                self.ty,
                self.tz
            ),
            homography
        )

        return img2screen(point)

    # --------------------------------------------------
    # Processing: getOffsetFromID()
    # --------------------------------------------------

    def get_offset_from_id(
        self,
        target_id
    ):

        index = -1

        for i, marker_id in enumerate(self.ids):

            if marker_id == target_id:
                index = i
                break

        if index >= 0:
            return self.offs[index]

        return PVector(0, 0, 0)
        
        