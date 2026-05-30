# managers/tag_manager.py

import math
import numpy as np
import pygame

from models.tag import Tag
from models.tagged_object import TaggedObject

from tools import (
    img2screen,
    transform_point,
    distance_point_to_plane,
    is_corner
)


class TagManager:

    def __init__(self, n, to_ids, to_offs):

        self.TAG_D = 150
        self.TO_D = 150

        self.tags = [Tag(i) for i in range(n)]

        self.tagged_objects = []

        self.active_tags = []
        self.active_tos = []

        for ids, offs in zip(to_ids, to_offs):
            self.tagged_objects.append(
                TaggedObject(ids, offs)
            )

    # -----------------------------------------------------
    # Processing set(...)
    # -----------------------------------------------------

    def set(
        self,
        marker_id,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz,
        corners
    ):
        self.tags[marker_id].set(
            tx,
            ty,
            tz,
            rx,
            ry,
            rz,
            corners
        )

    # -----------------------------------------------------
    # Rotation matrices
    # -----------------------------------------------------

    @staticmethod
    def rot_x(a):

        c = math.cos(a)
        s = math.sin(a)

        return np.array([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ])

    @staticmethod
    def rot_y(a):

        c = math.cos(a)
        s = math.sin(a)

        return np.array([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ])

    @staticmethod
    def rot_z(a):

        c = math.cos(a)
        s = math.sin(a)

        return np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])

    # -----------------------------------------------------
    # Processing update()
    # -----------------------------------------------------

    def update(self):

        self.active_tags.clear()
        self.active_tos.clear()

        for tag in self.tags:

            tag.check_active()

            if tag.active:
                self.active_tags.append(tag.id)

        for bundle in self.tagged_objects:

            active_bundle_tags = []

            for marker_id in bundle.ids:

                if self.tags[marker_id].active:
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
                        tag.id
                    )

                    # -------------------------
                    # Processing:
                    #
                    # v = (0,0,offset.z)
                    #
                    # R1.rotateZ(-rz)
                    # R1.rotateX(rx)
                    # R1.rotateY(ry)
                    # R1.rotateZ(rz)
                    # -------------------------

                    v = np.array([
                        0.0,
                        0.0,
                        offset.z
                    ])

                    R1 = (
                        self.rot_z(-tag.rz)
                        @ self.rot_x(tag.rx)
                        @ self.rot_y(tag.ry)
                        @ self.rot_z(tag.rz)
                    )

                    rotated_v = R1 @ v

                    P = np.array([
                        O[0] - rotated_v[0],
                        O[1] + rotated_v[1],
                        O[2] + rotated_v[2]
                    ])

                    # -------------------------
                    # Processing:
                    #
                    # w=(offset.x,offset.y,0)
                    #
                    # R2.rotateX(rx)
                    # R2.rotateY(ry)
                    # R2.rotateZ(rz)
                    # -------------------------

                    w = np.array([
                        offset.x,
                        offset.y,
                        0.0
                    ])

                    R2 = (
                        self.rot_x(tag.rx)
                        @ self.rot_y(tag.ry)
                        @ self.rot_z(tag.rz)
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

        for i, bundle in enumerate(
            self.tagged_objects
        ):
            if bundle.active:
                self.active_tos.append(i)

    # -----------------------------------------------------
    # Processing getActiveTOs()
    # -----------------------------------------------------

    def get_active_tos(self):

        result = []

        for idx in self.active_tos:
            result.append(
                self.tagged_objects[idx]
            )

        return result

    # -----------------------------------------------------
    # Processing getBundle()
    # -----------------------------------------------------

    def get_bundle(self, to_id):

        for bundle in self.get_active_tos():

            for marker_id in bundle.ids:

                if marker_id == to_id:
                    return bundle

        return None

    # -----------------------------------------------------
    # Processing getActiveTags()
    # -----------------------------------------------------

    def get_active_tags(self):

        result = []

        for tag_id in self.active_tags:
            result.append(
                self.tags[tag_id]
            )

        return result

    # -----------------------------------------------------
    # Processing displayRaw()
    # -----------------------------------------------------

    def display_raw(self, surface):

        for tag in self.tags:

            if not tag.active:
                continue

            for corner in tag.corners:

                pygame.draw.circle(
                    surface,
                    (255, 255, 255),
                    (int(corner.x), int(corner.y)),
                    4
                )

    # -----------------------------------------------------
    # Processing drawTagSimple()
    # -----------------------------------------------------

    def draw_tag_simple(
        self,
        surface,
        marker_id,
        loc2d,
        angle2d,
        diameter,
        color_rgb=(100, 100, 100)
    ):

        x, y = loc2d

        radius = diameter / 2

        if radius < 1:
            return

        pygame.draw.circle(
            surface,
            color_rgb,
            (int(x), int(y)),
            int(radius)
        )

        x2 = x + radius * math.cos(angle2d)
        y2 = y + radius * math.sin(angle2d)

        pygame.draw.line(
            surface,
            (0, 0, 0),
            (int(x), int(y)),
            (int(x2), int(y2)),
            3
        )

    # -----------------------------------------------------
    # Processing drawTagCustom()
    # -----------------------------------------------------

    def draw_tag_custom(
        self,
        surface,
        marker_id,
        loc2d,
        angle2d
    ):

        x, y = loc2d

        radius = 50

        pygame.draw.circle(
            surface,
            (52, 52, 52),
            (int(x), int(y)),
            radius
        )

        px = x + radius * math.cos(angle2d)
        py = y + radius * math.sin(angle2d)

        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (int(px), int(py)),
            radius // 4
        )

    # -----------------------------------------------------
    # Processing drawActiveTags()
    # -----------------------------------------------------

    def draw_active_tags(
        self,
        surface,
        homography,
        plane_points,
        touch_threshold,
        global_rz
    ):

        for tag in self.get_active_tags():

            if is_corner(tag.id):
                continue

            p = transform_point(
                (tag.tx, tag.ty, tag.tz),
                homography
            )

            loc2d = img2screen(p)

            self.draw_tag_simple(
                surface,
                tag.id,
                loc2d,
                tag.rz - global_rz,
                self.TAG_D
            )

    # -----------------------------------------------------
    # Processing drawActiveTOs()
    # -----------------------------------------------------

    def draw_active_tos(
        self,
        surface,
        homography,
        plane_points,
        touch_threshold,
        global_rz
    ):

        for bundle in self.get_active_tos():

            p = transform_point(
                (bundle.tx, bundle.ty, bundle.tz),
                homography
            )

            loc2d = img2screen(p)

            self.draw_tag_simple(
                surface,
                bundle.ids[0],
                loc2d,
                bundle.rz - global_rz,
                self.TO_D,
                (0, 127, 255)
            )

    # -----------------------------------------------------
    # Processing drawCustomActiveBundles()
    # -----------------------------------------------------

    def draw_custom_active_bundles(
        self,
        surface,
        homography,
        plane_points,
        touch_threshold,
        global_rz
    ):

        for bundle in self.get_active_tos():

            distance = distance_point_to_plane(
                (bundle.tx, bundle.ty, bundle.tz),
                plane_points
            )

            if distance < touch_threshold:

                p = transform_point(
                    (bundle.tx, bundle.ty, bundle.tz),
                    homography
                )

                loc2d = img2screen(p)

                self.draw_tag_custom(
                    surface,
                    bundle.ids[0],
                    loc2d,
                    bundle.rz - global_rz
                )