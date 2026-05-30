"""
api.py

Port of API.pde

ArUco-TUI Client v26.1
Processing -> Python
"""

from tools import PVector
import tools

# ============================================================
# Debug
# ============================================================

serialDebug = False

# ============================================================
# Global references
# встановлюються з main.py
# ============================================================

tm = None
DOlist = None


def initialize_api(tag_manager, data_objects):
    """
    Викликається один раз після створення TagManager
    та DataObjects.
    """

    global tm
    global DOlist

    tm = tag_manager
    DOlist = data_objects


# ============================================================
# Helpers
# ============================================================

def _get_screen_position(x, y, z):
    """
    Processing:
    img2screen(
        transformPoint(
            new PVector(x,y,z),
            homography
        )
    )
    """

    world = PVector(x, y, z)

    transformed = tools.transform_point(
        world,
        tools.homography
    )

    return tools.img2screen(transformed)


# ============================================================
# TAG EVENTS
# ============================================================

def tag_present_3d(
    marker_id,
    tx,
    ty,
    tz,
    rx,
    ry,
    rz
):

    if serialDebug and marker_id != 0:

        print(
            f"+ Tag: {marker_id} "
            f"loc=({tx:.4f}, {ty:.4f}, {tz:.4f}) "
            f"angle=({rx:.4f}, {ry:.4f}, {rz:.4f})"
        )


def tag_absent_3d(
    marker_id,
    tx,
    ty,
    tz,
    rx,
    ry,
    rz
):

    if serialDebug and marker_id != 0:

        print(
            f"- Tag: {marker_id} "
            f"loc=({tx:.4f}, {ty:.4f}, {tz:.4f}) "
            f"angle=({rx:.4f}, {ry:.4f}, {rz:.4f})"
        )


def tag_update_3d(
    marker_id,
    tx,
    ty,
    tz,
    rx,
    ry,
    rz
):

    if serialDebug and marker_id != 0:

        print(
            f"% Tag: {marker_id} "
            f"loc=({tx:.4f}, {ty:.4f}, {tz:.4f}) "
            f"angle=({rx:.4f}, {ry:.4f}, {rz:.4f})"
        )


# ============================================================
# TAGGED OBJECT EVENTS
# ============================================================

def to_present_2d(
    object_id,
    x,
    y,
    z,
    rz
):

    if not tools.homographyMatrixCalculated:
        return

    if tools.is_corner(object_id):
        return

    if tm is None:
        return

    if DOlist is None:
        return

    t = _get_screen_position(x, y, z)

    if serialDebug:

        print(
            f"+ Bundle: {object_id} "
            f"loc=({t.x:.1f}, {t.y:.1f}) "
            f"angle={rz:.4f}"
        )

    for obj in DOlist:

        if obj.check_hit(
            t.x,
            t.y,
            tm.TO_D / 2
        ):

            if not obj.has_ctrl_id(object_id):

                obj.add_ctrl_id(
                    object_id,
                    PVector(t.x, t.y),
                    rz
                )


def to_absent_2d(
    object_id,
    x,
    y,
    z,
    rz
):

    if not tools.homographyMatrixCalculated:
        return

    if tools.is_corner(object_id):
        return

    if DOlist is None:
        return

    t = _get_screen_position(x, y, z)

    if serialDebug:

        print(
            f"- Bundle: {object_id} "
            f"loc=({t.x:.1f}, {t.y:.1f}) "
            f"angle={rz:.4f}"
        )

    for obj in DOlist:

        if obj.has_ctrl_id(object_id):

            if hasattr(obj, "set_previous_rotation"):
                obj.set_previous_rotation(
                    obj.rotation
                )

            obj.remove_ctrl_id(
                object_id
            )


def to_update_2d(
    object_id,
    x,
    y,
    z,
    rz
):

    if not tools.homographyMatrixCalculated:
        return

    if tools.is_corner(object_id):
        return

    if DOlist is None:
        return

    t = _get_screen_position(x, y, z)

    if serialDebug:

        print(
            f"% Bundle: {object_id} "
            f"loc=({t.x:.1f}, {t.y:.1f}) "
            f"angle={rz:.4f}"
        )

    #
    # В оригінальному Processing:
    #
    # if (obj.hasCtrlID(id)) {
    #
    # }
    #
    # Блок порожній.
    #
    # Тому навмисно нічого не робимо.
    #

    return


# ============================================================
# Backward compatibility
# ============================================================

Tag_Present3D = tag_present_3d
Tag_Update3D = tag_update_3d
Tag_Absent3D = tag_absent_3d

TO_Present2D = to_present_2d
TO_Update2D = to_update_2d
TO_Absent2D = to_absent_2d
