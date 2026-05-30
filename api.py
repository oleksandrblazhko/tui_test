"""
api.py

Port of API.pde

ArUco-TUI Client v26.1
Processing -> Python
"""

from tools import (
    PVector,
    transform_point,
    img2screen,
    global_rz,
    homographyMatrixCalculated
)


# ============================================================
# Debug flags
# ============================================================

serialDebug = False


# ============================================================
# Global references
# Будуть встановлені з main.py
# ============================================================

tm = None
DOlist = None


def initialize_api(tag_manager, data_objects):
    """
    Викликається один раз з main.py
    """

    global tm
    global DOlist

    tm = tag_manager
    DOlist = data_objects


# ============================================================
# TAG EVENTS
# ============================================================

def Tag_Present3D(
        marker_id,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz):

    if serialDebug and marker_id != 0:

        print(
            f"+ Tag {marker_id}: "
            f"loc=({tx:.4f},{ty:.4f},{tz:.4f}) "
            f"angle=({rx:.4f},{ry:.4f},{rz:.4f})"
        )


def Tag_Absent3D(
        marker_id,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz):

    if serialDebug and marker_id != 0:

        print(
            f"- Tag {marker_id}: "
            f"loc=({tx:.4f},{ty:.4f},{tz:.4f}) "
            f"angle=({rx:.4f},{ry:.4f},{rz:.4f})"
        )


def Tag_Update3D(
        marker_id,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz):

    if serialDebug and marker_id != 0:

        print(
            f"% Tag {marker_id}: "
            f"loc=({tx:.4f},{ty:.4f},{tz:.4f}) "
            f"angle=({rx:.4f},{ry:.4f},{rz:.4f})"
        )


# ============================================================
# TAGGED OBJECT EVENTS
# ============================================================

def TO_Present2D(
        object_id,
        x,
        y,
        z,
        rz):

    if not homographyMatrixCalculated:
        return

    if is_corner(object_id):
        return

    t = img2screen(
        transform_point(
            PVector(x, y, z)
        )
    )

    if serialDebug:

        print(
            f"+ Bundle {object_id}: "
            f"loc=({t.x:.1f},{t.y:.1f}) "
            f"angle={rz:.3f}"
        )

    for obj in DOlist:

        if obj.check_hit(
                t.x,
                t.y,
                tm.TO_D / 2):

            if not obj.has_ctrl_id(object_id):

                obj.add_ctrl_id(
                    object_id,
                    PVector(t.x, t.y),
                    rz
                )


def TO_Absent2D(
        object_id,
        x,
        y,
        z,
        rz):

    if not homographyMatrixCalculated:
        return

    if is_corner(object_id):
        return

    t = img2screen(
        transform_point(
            PVector(x, y, z)
        )
    )

    if serialDebug:

        print(
            f"- Bundle {object_id}: "
            f"loc=({t.x:.1f},{t.y:.1f}) "
            f"angle={rz:.3f}"
        )

    for obj in DOlist:

        if obj.has_ctrl_id(object_id):

            obj.set_previous_rotation(
                obj.rotation
            )

            obj.remove_ctrl_id(
                object_id
            )


def TO_Update2D(
        object_id,
        x,
        y,
        z,
        rz):

    if not homographyMatrixCalculated:
        return

    if is_corner(object_id):
        return

    t = img2screen(
        transform_point(
            PVector(x, y, z)
        )
    )

    if serialDebug:

        print(
            f"% Bundle {object_id}: "
            f"loc=({t.x:.1f},{t.y:.1f}) "
            f"angle={rz:.3f}"
        )

    for obj in DOlist:

        if obj.has_ctrl_id(object_id):

            #
            # Оригінальний Processing код:
            #
            # if (obj.hasCtrlID(id)) {
            #
            # }
            #
            # тобто порожній блок.
            #
            # Тому тут також нічого не робимо.
            #

            pass


# ============================================================
# Helpers
# ============================================================

def is_corner(marker_id):
    """
    Аналог tools.isCorner()

    Поки що кути жорстко задані,
    надалі можна винести у config.py
    """

    return marker_id in (1, 2, 3)