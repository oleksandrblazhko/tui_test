"""
main.py

Port of:

ArUco-TUI Client v26.1

Processing -> Python
"""

import math
import time

import pygame

import tools

from tools import (
    PVector,
    img2screen,
    transform_point,
    unwrap_angle
)

from tag_manager import TagManager
from data_object import DataObject

from continuous_gestures import (
    DO_setValue,
    DO_setValueLoc2D,
    DO_setLocOri2D
)

from api import initialize_api


# ============================================================
# CONFIG
# ============================================================

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

FPS = 60

gestureMode = 2

touchThreshold = 0.01

paperWidthOnScreen = 193.5
markerWidth = 15.0


# ============================================================
# TO CONFIG
# ============================================================

TO_IDS = [
    [48],
    [49],
    [50],
    [51]
]

TO_OFFSETS = [
    [PVector(0, 0, -0.025)],
    [PVector(0, 0, -0.025)],
    [PVector(0, 0, -0.025)],
    [PVector(0, 0, -0.025)]
]


# ============================================================
# GLOBALS
# ============================================================

DOlist = []

tm = None

running = True

screen = None
clock = None


# ============================================================
# DATA OBJECTS
# ============================================================

def init_data_objects():

    global DOlist

    DOlist.clear()

    dataObjSize = 200

    DOlist.append(
        DataObject(
            0,
            False,
            10,
            WINDOW_WIDTH/2-dataObjSize,
            WINDOW_HEIGHT/2-dataObjSize,
            dataObjSize,
            "Obj. 1"
        )
    )

    DOlist.append(
        DataObject(
            1,
            False,
            10,
            WINDOW_WIDTH/2+dataObjSize,
            WINDOW_HEIGHT/2-dataObjSize,
            dataObjSize,
            "Obj. 2"
        )
    )

    DOlist.append(
        DataObject(
            2,
            False,
            10,
            WINDOW_WIDTH/2-dataObjSize,
            WINDOW_HEIGHT/2+dataObjSize,
            dataObjSize,
            "Obj. 3"
        )
    )

    DOlist.append(
        DataObject(
            3,
            False,
            10,
            WINDOW_WIDTH/2+dataObjSize,
            WINDOW_HEIGHT/2+dataObjSize,
            dataObjSize,
            "Obj. 4"
        )
    )


# ============================================================
# SETUP
# ============================================================

def setup():

    global screen
    global clock
    global tm

    pygame.init()

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    pygame.display.set_caption(
        "ArUco-TUI Python"
    )

    clock = pygame.time.Clock()

    tm = TagManager(
        600,
        TO_IDS,
        TO_OFFSETS
    )

    init_data_objects()

    initialize_api(
        tm,
        DOlist
    )

    tools.load_calibration_file(
        "corners.txt"
    )


# ============================================================
# UPDATE OBJECTS
# ============================================================

def update_all_data_objects(
        output_mode):

    for obj in DOlist:

        if obj.multiControl:
            continue

        num_blobs = obj.get_ctrl_counts()

        if num_blobs <= 0:

            if obj.bEngaged:

                obj.val += obj.tempVal

                obj.tempVal = 0

                obj.get_st_gesture_type()

                obj.bEngaged = False

        else:

            m = PVector()
            theta = 0

            target_id = obj.ctrlIDList[0]

            for bundle in tm.get_active_tos():

                if bundle.get_to_id() == target_id:

                    m = img2screen(
                        transform_point(
                            PVector(
                                bundle.tx,
                                bundle.ty,
                                bundle.tz
                            )
                        )
                    )

                    theta = (
                        bundle.rz -
                        tools.global_rz
                    )

            if not obj.bEngaged:

                obj.theta0 = (
                    theta -
                    obj.prev_rotation
                )

                obj.theta_p = obj.theta0

                obj.m0 = PVector(
                    m.x,
                    m.y
                )

                obj.bEngaged = True

                obj.gestureType = (
                    obj.UNDEFINED
                )

                obj.numTouches = (
                    num_blobs
                )

                obj.lastCtrlID = (
                    target_id
                )

                obj.gesturePerformed = True

            else:

                new_angle = unwrap_angle(
                    theta,
                    obj.theta_p
                )

                obj.rotation = -(
                    obj.theta0 -
                    new_angle
                )

                obj.theta_p = new_angle

                obj.translation = (
                    PVector(
                        m.x - obj.m0.x,
                        m.y - obj.m0.y
                    )
                )

                if (
                    num_blobs >
                    obj.numTouches
                ):
                    obj.numTouches = (
                        num_blobs
                    )

                if output_mode == 1:

                    DO_setValue(
                        obj.dataID,
                        obj.lastCtrlID,
                        DOlist
                    )

                elif output_mode == 2:

                    DO_setValueLoc2D(
                        obj.dataID,
                        obj.lastCtrlID,
                        DOlist,
                        tm,
                        tools.homography
                    )

                elif output_mode == 3:

                    DO_setLocOri2D(
                        obj.dataID,
                        obj.lastCtrlID,
                        DOlist,
                        tm,
                        tools.homography
                    )


# ============================================================
# DISPLAY
# ============================================================

def display_ui():

    font = pygame.font.SysFont(
        None,
        32
    )

    for obj in DOlist:

        rect = pygame.Rect(
            obj.x - obj.w/2,
            obj.y - obj.h/2,
            obj.w,
            obj.h
        )

        pygame.draw.rect(
            screen,
            (250, 177, 160),
            rect
        )

        value = str(
            int(
                obj.val +
                obj.tempVal
            )
        )

        label = (
            f"({obj.dataID})"
            f"{obj.name}:"
            f"{value}"
        )

        txt1 = font.render(
            label,
            True,
            (30, 30, 30)
        )

        txt2 = font.render(
            value,
            True,
            (30, 30, 30)
        )

        screen.blit(
            txt1,
            (
                obj.x - obj.w/2,
                obj.y + obj.h/2 - 30
            )
        )

        screen.blit(
            txt2,
            (
                obj.x - 20,
                obj.y - 20
            )
        )


# ============================================================
# DRAW
# ============================================================

def draw():

    screen.fill(
        (100, 100, 100)
    )

    tm.update()

    update_all_data_objects(
        gestureMode
    )

    display_ui()

    pygame.display.flip()


# ============================================================
# LOOP
# ============================================================

def main_loop():

    global running

    while running:

        for event in pygame.event.get():

            if (
                event.type ==
                pygame.QUIT
            ):
                running = False

        draw()

        clock.tick(FPS)

    pygame.quit()


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":

    setup()

    main_loop()