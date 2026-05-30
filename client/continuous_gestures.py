"""
continuous_gestures.py

Port of ContinuousGestures.pde

ArUco-TUI Client v26.1
Processing -> Python
"""

import math

from tools import (
    PVector,
    transform_point,
    img2screen
)


# ============================================================
# Gesture Mode 1
# ============================================================

def DO_setValue(
        data_id,
        ctrl_id,
        DOlist):

    """
    Processing:

    void DO_setValue(int dataID, int ctrlID)
    """

    obj = DOlist[data_id]

    delta_rotation = (
        obj.rotation -
        obj.prev_rotation
    )

    value = map_rotation_to_value(
        math.degrees(delta_rotation)
    )

    obj.set_temp_val(value)


# ============================================================
# Gesture Mode 2
# ============================================================

def DO_setValueLoc2D(
        data_id,
        ctrl_id,
        DOlist,
        tm,
        homography):

    """
    Processing:

    void DO_setValueLoc2D(int dataID, int ctrlID)
    """

    obj = DOlist[data_id]

    bundle = tm.get_bundle(ctrl_id)

    if bundle is None:
        return

    loc2d = img2screen(
        transform_point(
            PVector(
                bundle.tx,
                bundle.ty,
                bundle.tz
            )
        )
    )

    delta_rotation = (
        obj.rotation -
        obj.prev_rotation
    )

    value = map_rotation_to_value(
        math.degrees(delta_rotation)
    )

    obj.set_temp_val(value)

    obj.update_loc2d(
        loc2d.x,
        loc2d.y
    )


# ============================================================
# Gesture Mode 3
# ============================================================

def DO_setLocOri2D(
        data_id,
        ctrl_id,
        DOlist,
        tm,
        homography):

    """
    Processing:

    void DO_setLocOri2D(int dataID, int ctrlID)
    """

    obj = DOlist[data_id]

    bundle = tm.get_bundle(ctrl_id)

    if bundle is None:
        return

    loc2d = img2screen(
        transform_point(
            PVector(
                bundle.tx,
                bundle.ty,
                bundle.tz
            )
        )
    )

    obj.update_loc2d(
        loc2d.x,
        loc2d.y
    )

    #
    # relative rotation
    #

    obj.update_ori2d(
        obj.rotation
    )


# ============================================================
# Utility Functions
# ============================================================

def map_rotation_to_value(
        rotation_deg,
        input_min=0.0,
        input_max=100.0,
        output_min=0.0,
        output_max=10.0):

    """
    Processing equivalent:

    map(rotation,0,100,0,10)
    """

    return (
        (rotation_deg - input_min)
        *
        (output_max - output_min)
        /
        (input_max - input_min)
        +
        output_min
    )


# ============================================================
# Dispatcher
# ============================================================

def process_continuous_gesture(
        gesture_mode,
        data_id,
        ctrl_id,
        DOlist,
        tm,
        homography):

    """
    Universal dispatcher

    Equivalent to:

    switch(output_mode)
    """

    if gesture_mode == 1:

        DO_setValue(
            data_id,
            ctrl_id,
            DOlist
        )

    elif gesture_mode == 2:

        DO_setValueLoc2D(
            data_id,
            ctrl_id,
            DOlist,
            tm,
            homography
        )

    elif gesture_mode == 3:

        DO_setLocOri2D(
            data_id,
            ctrl_id,
            DOlist,
            tm,
            homography
        )