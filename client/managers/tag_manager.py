"""
tag_manager.py

Port of TagManager.pde

ArUco-TUI Client v26.1
Processing -> Python
"""

import numpy as np

from tag import Tag
from tagged_object import TaggedObject

from tools import (
    PVector,
    transform_point,
    img2screen,
    distance_point_to_plane,
    planePoints,
    homography,
    homographyMatrixCalculated,
    global_rz,
    touchThreshold,
    is_corner
)


class TagManager:

    def __init__(
        self,
        num_tags,
        to_ids,
        to_offsets
    ):

        self.TAG_D = 150
        self.TO_D = 150

        self.tags = [
            Tag(i)
            for i in range(num_tags)
        ]

        self.tagged_objects = []

        self.active_tags = []
        self.active_tos = []

        for ids, offsets in zip(
            to_ids,
            to_offsets
        ):

            self.tagged_objects.append(
                TaggedObject(
                    ids,
                    offsets
                )
            )

    # =====================================================
    # TAG UPDATE
    # =====================================================

    def set(
        self,
        tag_id,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz,
        corners
    ):

        if (
            tag_id < 0 or
            tag_id >= len(self.tags)
        ):
            return

        self.tags[tag_id].set(
            tx,
            ty,
            tz,
            rx,
            ry,
            rz,
            corners
        )

    # =====================================================
    # ROTATION MATRICES
    # =====================================================

    @staticmethod
    def rotate_x(angle):

        c = np.cos(angle)
        s = np.sin(angle)

        return np.array([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ])

    @staticmethod
    def rotate_y(angle):

        c = np.cos(angle)
        s = np.sin(angle)

        return np.array([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ])

    @staticmethod
    def rotate_z(angle):

        c = np.cos(angle)
        s = np.sin(angle)

        return np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])

    # =====================================================
    # MAIN UPDATE
    # =====================================================

    def update(self):

        self.active_tags.clear()
        self.active_tos.clear()

        # ---------------------------------------------
        # active tags
        # ---------------------------------------------

        for tag in self.tags:

            tag.check_active()

            if tag.active:
                self.active_tags.append(
                    tag.tag_id
                )

        # ---------------------------------------------
        # bundles
        # ---------------------------------------------

        if not homographyMatrixCalculated:
            return

        for bundle in self.tagged_objects:

            active_bundle_tags = []

            for marker_id in bundle.ids:

                if (
                    marker_id < len(self.tags)
                    and
                    self.tags[marker_id].active
                ):
                    active_bundle_tags.append(
                        self.tags[marker_id]
                    )

            if len(active_bundle_tags) > 0:

                loc = np.zeros(3)
                ori = np.zeros(3)

                for tag in active_bundle_tags:

                    O = np.array([
                        tag.tx,
                        tag.ty,
                        tag.tz
                    ])

                    offset = bundle.get_offset_from_id(
                        tag.tag_id
                    )

                    # ---------------------------------
                    # R1
                    # ---------------------------------

                    v = np.array([
                        0,
                        0,
                        offset.z
                    ])

                    R1 = (
                        self.rotate_z(-tag.rz)
                        @
                        self.rotate_x(tag.rx)
                        @
                        self.rotate_y(tag.ry)
                        @
                        self.rotate_z(tag.rz)
                    )

                    rotated_v = R1 @ v

                    P = np.array([
                        O[0] - rotated_v[0],
                        O[1] + rotated_v[1],
                        O[2] + rotated_v[2]
                    ])

                    # ---------------------------------
                    # R2
                    # ---------------------------------

                    w = np.array([
                        offset.x,
                        offset.y,
                        0
                    ])

                    R2 = (
                        self.rotate_x(tag.rx)
                        @
                        self.rotate_y(tag.ry)
                        @
                        self.rotate_z(tag.rz)
                    )

                    rotated_w = R2 @ w

                    P_prime = np.array([
                        P[0] - rotated_w[0],
                        P[1] + rotated_w[1],
                        P[2] + rotated_w[2]
                    ])

                    loc += P_prime

                    ori += np.array([
                        tag.rx,
                        tag.ry,
                        tag.rz
                    ])

                loc /= len(active_bundle_tags)
                ori /= len(active_bundle_tags)

                bundle.set(
                    float(loc[0]),
                    float(loc[1]),
                    float(loc[2]),
                    float(ori[0]),
                    float(ori[1]),
                    float(ori[2])
                )

            else:

                bundle.set_inactive()

        for index, bundle in enumerate(
            self.tagged_objects
        ):

            if bundle.active:
                self.active_tos.append(index)

    # =====================================================
    # GETTERS
    # =====================================================

    def get_active_tos(self):

        return [
            self.tagged_objects[i]
            for i in self.active_tos
        ]

    def get_active_tags(self):

        return [
            self.tags[i]
            for i in self.active_tags
        ]

    def get_bundle(
        self,
        to_id
    ):

        for bundle in self.get_active_tos():

            for marker_id in bundle.ids:

                if marker_id == to_id:
                    return bundle

        return None

    # =====================================================
    # DEBUG DRAW
    # =====================================================

    def draw_active_tos(
        self,
        surface=None
    ):
        """
        Заглушка.

        Аналог drawActiveTOs().

        Реалізацію pygame краще
        винести окремо після завершення
        всіх математичних модулів.
        """
        pass

    def draw_active_tags(
        self,
        surface=None
    ):
        """
        Аналог drawActiveTags().
        """
        pass

    def display_raw(
        self,
        surface=None
    ):
        """
        Аналог displayRaw().
        """
        pass
        