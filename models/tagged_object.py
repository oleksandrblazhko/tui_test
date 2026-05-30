import math
import time

import numpy as np


class TaggedObject:

    def __init__(
        self,
        to_ids,
        offsets
    ):

        self.ttl = 100

        self.active = False

        self.timestamp = 0

        self.ids = list(to_ids)

        self.offsets = list(offsets)

        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0

        self.rx = 0.0
        self.ry = 0.0
        self.rz = 0.0

        self.p_rx = 0.0
        self.p_ry = 0.0
        self.p_rz = 0.0

    def get_to_id(self):

        return self.ids[0]

    def unwrap_angle(
        self,
        current_angle,
        previous_angle
    ):

        delta = current_angle - previous_angle

        if delta > math.pi:
            current_angle -= 2 * math.pi

        elif delta < -math.pi:
            current_angle += 2 * math.pi

        return current_angle

    def set_inactive(self):

        now = time.time() * 1000

        if self.active and (now - self.timestamp) > self.ttl:

            self.active = False

            from api import to_absent_2d

            to_absent_2d(
                self.get_to_id(),
                self.tx,
                self.ty,
                self.tz,
                self.rz
            )

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

        from api import (
            to_present_2d,
            to_update_2d,
            distance_point_to_plane
        )

        from config import (
            PLANE_POINTS,
            TOUCH_THRESHOLD
        )

        distance = distance_point_to_plane(
            np.array([tx, ty, tz]),
            PLANE_POINTS
        )

        if distance < TOUCH_THRESHOLD:

            if not self.active:

                to_present_2d(
                    self.get_to_id(),
                    tx,
                    ty,
                    tz,
                    self.rz
                )

            else:

                to_update_2d(
                    self.get_to_id(),
                    tx,
                    ty,
                    tz,
                    self.rz
                )

            self.active = True
            self.timestamp = time.time() * 1000

        else:

            self.set_inactive()

    def get_offset_from_id(
        self,
        target_id
    ):

        for i, tag_id in enumerate(self.ids):

            if tag_id == target_id:
                return self.offsets[i]

        return np.zeros(3)