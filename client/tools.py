"""
tools.py
Port of Processing tools.pde

ArUco-TUI Client v26.1
Processing -> Python migration
"""

import math
import numpy as np
import cv2
from dataclasses import dataclass


# ============================================================
# PVector replacement
# ============================================================

@dataclass
class PVector:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def copy(self):
        return PVector(self.x, self.y, self.z)

    def add(self, other):
        return PVector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def sub(self, other):
        return PVector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def mult(self, value):
        return PVector(
            self.x * value,
            self.y * value,
            self.z * value
        )

    def div(self, value):
        return PVector(
            self.x / value,
            self.y / value,
            self.z / value
        )


# ============================================================
# Global configuration
# ============================================================

paperWidthOnScreen = 193.5
markerWidth = 15.0

tag2screenRatio = 297.0 / paperWidthOnScreen

touchThreshold = 0.01

cornersID = [1, 3, 2, 0]

homographyMatrixCalculated = False

homography = None

srcPointsT = [None] * 4
dstPointsT = [None] * 4

srcPointsR = [None] * 4
dstPointsR = [None] * 4

planePoints = [None] * 4

global_rx = 0.0
global_ry = 0.0
global_rz = 0.0


# ============================================================
# Calibration geometry
# ============================================================

cCen = PVector(842 / 2.0, 595 / 2.0)

mW = (markerWidth / 25.4 * 72.0) * tag2screenRatio

calibgridWidth = 100 + markerWidth
calibgridHeight = 100 + markerWidth

mDC1 = (calibgridWidth / 2) * (72 / 25.4) * tag2screenRatio
mDC2 = (calibgridHeight / 2) * (72 / 25.4) * tag2screenRatio

markerX = [
    cCen.x - mDC1 + mW / 2,
    cCen.x - mDC1 + mW / 2,
    cCen.x + mDC2 - mW / 2,
    cCen.x + mDC2 - mW / 2
]

markerY = [
    cCen.y - mDC1 + mW / 2,
    cCen.y + mDC1 + mW / 2,
    cCen.y - mDC2 - mW / 2,
    cCen.y + mDC2 - mW / 2
]

markerGridWidth = markerX[2] - markerX[0]

markerOffset = PVector(markerX[0], markerY[0])
windowOffset = PVector(0, 0)
imageOffset = PVector(0, 0)


# ============================================================
# Calibration file
# ============================================================

def load_calibration_file(filename):

    cornerPointsT = []
    cornerPointsR = []

    with open(filename, "r") as f:

        for line in f:

            vals = [float(v.strip()) for v in line.split(",")]

            tx, ty, tz, rx, ry, rz = vals

            cornerPointsT.append(
                PVector(tx, ty, tz)
            )

            cornerPointsR.append(
                PVector(rx, ry, rz)
            )

    calculate_homography_matrix(cornerPointsT)

    register_plane_points()

    register_plane_orientation(cornerPointsR)

    global homographyMatrixCalculated
    homographyMatrixCalculated = True


def save_calibration_file(filename, tm):

    lines = []

    for idx in range(3):

        tag = tm.tags[cornersID[idx]]

        line = (
            f"{tag.tx:.6f},"
            f"{tag.ty:.6f},"
            f"{tag.tz:.6f},"
            f"{tag.rx:.6f},"
            f"{tag.ry:.6f},"
            f"{tag.rz:.6f}"
        )

        lines.append(line)

    with open(filename, "w") as f:
        f.write("\n".join(lines))


# ============================================================
# Homography
# ============================================================

def calculate_homography_matrix(corner_points):

    global homography

    src = np.array([
        [corner_points[0].x, corner_points[0].y],
        [corner_points[1].x, corner_points[1].y],
        [corner_points[2].x, corner_points[2].y]
    ], dtype=np.float32)

    dst = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0]
    ], dtype=np.float32)

    homography = cv2.getAffineTransform(src, dst)


def transform_point(point):

    global homography

    src = np.array([
        [point.x, point.y]
    ], dtype=np.float32)

    result = cv2.transform(
        np.array([src]),
        homography
    )[0][0]

    return PVector(
        float(result[0]),
        float(result[1]),
        0
    )


# ============================================================
# Plane registration
# ============================================================

def register_plane_points():

    global planePoints

    planePoints[0] = srcPointsT[0]
    planePoints[1] = srcPointsT[1]
    planePoints[2] = srcPointsT[2]


def register_plane_orientation(pointsR=None):

    global global_rx
    global global_ry
    global global_rz

    if pointsR is None:
        return

    global_rx = (
        pointsR[0].x +
        pointsR[1].x +
        pointsR[2].x
    ) / 3.0

    global_ry = (
        pointsR[0].y +
        pointsR[1].y +
        pointsR[2].y
    ) / 3.0

    global_rz = (
        pointsR[0].z +
        pointsR[1].z +
        pointsR[2].z
    ) / 3.0


# ============================================================
# Coordinate transforms
# ============================================================

def img2screen(p):

    return PVector(
        p.x * markerGridWidth
        + windowOffset.x
        + imageOffset.x
        + markerOffset.x,

        p.y * markerGridWidth
        + windowOffset.y
        + imageOffset.y
        + markerOffset.y,

        0
    )


# ============================================================
# Plane distance
# ============================================================

def subtract(v1, v2):

    return PVector(
        v1.x - v2.x,
        v1.y - v2.y,
        v1.z - v2.z
    )


def cross(v1, v2):

    return PVector(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )


def dot(v1, v2):

    return (
        v1.x * v2.x +
        v1.y * v2.y +
        v1.z * v2.z
    )


def distance_point_to_plane(point, plane_points):

    normal = cross(
        subtract(plane_points[1], plane_points[0]),
        subtract(plane_points[2], plane_points[0])
    )

    d = -dot(normal, plane_points[0])

    numerator = abs(
        dot(normal, point) + d
    )

    denominator = math.sqrt(
        normal.x ** 2 +
        normal.y ** 2 +
        normal.z ** 2
    )

    return numerator / denominator


# ============================================================
# Geometry helpers
# ============================================================

def get_distance_between(p0, p1):

    return math.sqrt(
        (p1.x - p0.x) ** 2 +
        (p1.y - p0.y) ** 2
    )


def get_angle_between(p0, p1):

    return math.atan2(
        p1.y - p0.y,
        p1.x - p0.x
    )


def get_centroid_between(p0, p1):

    return PVector(
        (p0.x + p1.x) / 2,
        (p0.y + p1.y) / 2
    )


def mm_to_px(mm):

    return (
        mm *
        (72.0 / 25.4) *
        tag2screenRatio
    )


# ============================================================
# Angle helpers
# ============================================================

def unwrap_angle(current, previous):

    delta = previous - current

    rotations = round(
        delta / (2 * math.pi)
    )

    return current + rotations * (
        2 * math.pi
    )


# ============================================================
# TO lookup
# ============================================================

def whichTO(marker_id, TO_IDS):

    for idx, ids in enumerate(TO_IDS):

        if ids[0] == marker_id:
            return idx

    return -1


# ============================================================
# Rotation matrix
# ============================================================

def get_rotation_matrix(
        roll,
        pitch,
        yaw):

    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll), math.cos(roll)]
    ])

    Ry = np.array([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)]
    ])

    Rz = np.array([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ])

    return Rz @ Ry @ Rx


def get_tilt_angles(
        tilt2D,
        angle2D):

    surf = np.array([
        tilt2D.x,
        tilt2D.y,
        angle2D
    ])

    obj = np.array([
        global_rx,
        global_ry,
        global_rz
    ])

    Rs = get_rotation_matrix(
        surf[0],
        surf[1],
        surf[2]
    )

    Ro = get_rotation_matrix(
        obj[0],
        obj[1],
        obj[2]
    )

    Rrel = Rs.T @ Ro

    tilt_x = math.atan2(
        Rrel[2, 1],
        Rrel[2, 2]
    )

    tilt_y = math.atan2(
        -Rrel[2, 0],
        math.sqrt(
            Rrel[2, 1]**2 +
            Rrel[2, 2]**2
        )
    )

    rel_roll = math.atan2(
        Rrel[1, 0],
        Rrel[0, 0]
    )

    return PVector(
        tilt_x,
        -tilt_y,
        rel_roll
    )