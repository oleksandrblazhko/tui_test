# tools.py
#
# ArUcoTUI Client v26.1
# Processing tools.pde -> Python
#

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


# ============================================================
# DEBUG FLAGS
# ============================================================

resetData = False
gestureDebug = False
dataObjectDebug = False
tagDebug = False
serialDebug = False

drawing = False


# ============================================================
# PVECTOR
# ============================================================

@dataclass
class PVector:

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def copy(self):
        return PVector(
            self.x,
            self.y,
            self.z
        )

    def set(self, x, y=None, z=None):

        if isinstance(x, PVector):

            self.x = x.x
            self.y = x.y
            self.z = x.z

        else:

            self.x = x

            if y is not None:
                self.y = y

            if z is not None:
                self.z = z

        return self

    def add(self, other):

        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def sub(self, other):

        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

        return self

    def mult(self, value):

        self.x *= value
        self.y *= value
        self.z *= value

        return self

    def div(self, value):

        if value != 0:

            self.x /= value
            self.y /= value
            self.z /= value

        return self

    def mag(self):

        return math.sqrt(
            self.x * self.x +
            self.y * self.y +
            self.z * self.z
        )

    def normalize(self):

        m = self.mag()

        if m > 0:
            self.div(m)

        return self

    @staticmethod
    def add_vectors(v1, v2):

        return PVector(
            v1.x + v2.x,
            v1.y + v2.y,
            v1.z + v2.z
        )

    @staticmethod
    def sub_vectors(v1, v2):

        return PVector(
            v1.x - v2.x,
            v1.y - v2.y,
            v1.z - v2.z
        )

    @staticmethod
    def mult_vector(v, scalar):

        return PVector(
            v.x * scalar,
            v.y * scalar,
            v.z * scalar
        )

    @staticmethod
    def div_vector(v, scalar):

        if scalar == 0:
            return v.copy()

        return PVector(
            v.x / scalar,
            v.y / scalar,
            v.z / scalar
        )


# ============================================================
# PMATRIX3D
# ============================================================

class PMatrix3D:

    def __init__(self):

        self.matrix = np.identity(4)

    def rotateX(self, angle):

        c = math.cos(angle)
        s = math.sin(angle)

        R = np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])

        self.matrix = self.matrix @ R

    def rotateY(self, angle):

        c = math.cos(angle)
        s = math.sin(angle)

        R = np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])

        self.matrix = self.matrix @ R

    def rotateZ(self, angle):

        c = math.cos(angle)
        s = math.sin(angle)

        R = np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.matrix = self.matrix @ R

    def mult(self, vector, result=None):

        vec = np.array([
            vector.x,
            vector.y,
            vector.z,
            1.0
        ])

        out = self.matrix @ vec

        if result is None:

            return PVector(
                float(out[0]),
                float(out[1]),
                float(out[2])
            )

        result.x = float(out[0])
        result.y = float(out[1])
        result.z = float(out[2])

    def transpose(self):

        self.matrix = self.matrix.T

    def apply(self, other):

        self.matrix = self.matrix @ other.matrix

    def set(self, other):

        self.matrix = other.matrix.copy()


# ============================================================
# GLOBAL CONFIG
# ============================================================

paperWidthOnScreen = 193.5
markerWidth = 15.0

touchThreshold = 0.01

cornersID = [1, 3, 2, 0]

srcPointsT = [None] * 4
dstPointsT = [None] * 4

srcPointsR = [None] * 4
dstPointsR = [None] * 4

planePoints = [None] * 4

homographyMatrixCalculated = False
homography = None

idTOs = []
offsetTOs = []

calibImg = None

global_rx = 0.0
global_ry = 0.0
global_rz = 0.0

alpha = 0.0


# ============================================================
# CALIBRATION GEOMETRY
# ============================================================

tag2screenRatio = 297.0 / paperWidthOnScreen

cCen = PVector(
    842.0 / 2.0,
    595.0 / 2.0
)

mW = (
    markerWidth / 25.4 * 72.0
) * tag2screenRatio

calibgridWidth = 100 + markerWidth
calibgridHeight = 100 + markerWidth

mDC1 = (
    calibgridWidth / 2.0
) * (
    72.0 / 25.4
) * tag2screenRatio

mDC2 = (
    calibgridHeight / 2.0
) * (
    72.0 / 25.4
) * tag2screenRatio

markerX = [
    cCen.x - mDC1 + mW / 2,
    cCen.x - mDC1 + mW / 2,
    cCen.x + mDC2 - mW / 2,
    cCen.x + mDC2 - mW / 2,
]

markerY = [
    cCen.y - mDC1 + mW / 2,
    cCen.y + mDC1 + mW / 2,
    cCen.y - mDC2 - mW / 2,
    cCen.y + mDC2 - mW / 2,
]

markerGridWidth = (
    markerX[2] -
    markerX[0]
)

markerOffset = PVector(
    markerX[0],
    markerY[0]
)

windowOffset = PVector(
    0,
    0
)

imageOffset = PVector(
    0,
    0
)

# ============================================================
# GLOBAL OBJECTS
# ============================================================

calibImg = None

homographyMatrixCalculated = False
homography = None

global_rx = 0.0
global_ry = 0.0
global_rz = 0.0

idTOs = []
offsetTOs = []


# ============================================================
# TAG MANAGER INITIALIZATION
# ============================================================

def init_tag_manager(
    tag_manager_class,
    to_ids,
    to_offsets,
    tag_count=600,
):
    """
    Processing:

    void initTagManager()
    """

    global idTOs
    global offsetTOs

    idTOs = []
    offsetTOs = []

    for ids, offs in zip(to_ids, to_offsets):

        idTOs.append(list(ids))
        offsetTOs.append(list(offs))

    return tag_manager_class(
        tag_count,
        idTOs,
        offsetTOs,
    )


# ============================================================
# CALIBRATION IMAGE
# ============================================================

def load_calibration_img(
    filename,
    screen_width,
    screen_height,
):
    """
    Processing:

    void loadCalibrationImg(String s)
    """

    global calibImg
    global imageOffset

    calibImg = cv2.imread(str(filename))

    if calibImg is None:
        raise FileNotFoundError(filename)

    h, w = calibImg.shape[:2]

    imageOffset.x = (screen_width - w) / 2.0
    imageOffset.y = (screen_height - h) / 2.0


# ============================================================
# CALIBRATION FILE
# ============================================================

def load_calibration_file(filename):
    """
    Processing:

    void loadCalibrationFile(String filename)
    """

    global homographyMatrixCalculated

    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(filename)

    lines = path.read_text().splitlines()

    cornerPointsT = []
    cornerPointsR = []

    for line in lines:

        values = [
            float(v.strip())
            for v in line.split(",")
        ]

        tx, ty, tz, rx, ry, rz = values

        cornerPointsT.append(
            PVector(tx, ty, tz)
        )

        cornerPointsR.append(
            PVector(rx, ry, rz)
        )

    calculate_homography_matrix(
        cornerPointsT
    )

    register_plane_points()

    register_plane_orientation(
        cornerPointsR
    )

    homographyMatrixCalculated = True


def save_calibration_file(
    filename,
    tag_manager,
):
    """
    Processing:

    void saveCalibrationFile(String filename)
    """

    lines = []

    for i in range(3):

        tag = tag_manager.tags[
            cornersID[i]
        ]

        lines.append(
            f"{tag.tx:.3f}, "
            f"{tag.ty:.3f}, "
            f"{tag.tz:.3f}, "
            f"{tag.rx:.3f}, "
            f"{tag.ry:.3f}, "
            f"{tag.rz:.3f}"
        )

    Path(filename).write_text(
        "\n".join(lines)
    )


# ============================================================
# HOMOGRAPHY
# ============================================================

def calculate_homography(
    src_points,
    dst_points,
):
    """
    Processing:

    SimpleMatrix calculateHomography(...)
    """

    src_matrix = np.zeros(
        (3, 3),
        dtype=np.float64
    )

    dst_matrix = np.zeros(
        (3, 3),
        dtype=np.float64
    )

    for i in range(3):

        src_matrix[0, i] = src_points[i].x
        src_matrix[1, i] = src_points[i].y
        src_matrix[2, i] = src_points[i].z

        dst_matrix[0, i] = dst_points[i].x
        dst_matrix[1, i] = dst_points[i].y
        dst_matrix[2, i] = 1.0

    return (
        dst_matrix
        @
        np.linalg.pinv(src_matrix)
    )


# ============================================================
# HOMOGRAPHY FROM FILE
# ============================================================

def calculate_homography_matrix(
    corner_points
):
    """
    Processing:

    calculateHomographyMatrix(
        PVector[] cornerPointsT
    )
    """

    global homography

    srcPointsT[0] = corner_points[0].copy()
    srcPointsT[1] = corner_points[1].copy()
    srcPointsT[2] = corner_points[2].copy()

    dstPointsT[0] = PVector(0, 0)
    dstPointsT[1] = PVector(1, 0)
    dstPointsT[2] = PVector(1, 1)

    homography = calculate_homography(
        srcPointsT,
        dstPointsT
    )

    return homography


# ============================================================
# HOMOGRAPHY FROM ACTIVE CORNERS
# ============================================================

def calculate_homography_matrix_live(
    tag_manager
):
    """
    Processing:

    calculateHomographyMatrix()
    """

    global homography

    srcPointsT[0] = PVector(
        tag_manager.tags[
            cornersID[0]
        ].tx,
        tag_manager.tags[
            cornersID[0]
        ].ty,
        tag_manager.tags[
            cornersID[0]
        ].tz,
    )

    srcPointsT[1] = PVector(
        tag_manager.tags[
            cornersID[1]
        ].tx,
        tag_manager.tags[
            cornersID[1]
        ].ty,
        tag_manager.tags[
            cornersID[1]
        ].tz,
    )

    srcPointsT[2] = PVector(
        tag_manager.tags[
            cornersID[2]
        ].tx,
        tag_manager.tags[
            cornersID[2]
        ].ty,
        tag_manager.tags[
            cornersID[2]
        ].tz,
    )

    dstPointsT[0] = PVector(0, 0)
    dstPointsT[1] = PVector(1, 0)
    dstPointsT[2] = PVector(1, 1)

    homography = calculate_homography(
        srcPointsT,
        dstPointsT
    )

    return homography


# ============================================================
# HOMOGRAPHY TRANSFORM
# ============================================================

def transform_point(
    point,
    H=None
):
    """
    Processing:

    PVector transformPoint(...)
    """

    if H is None:
        H = homography

    vec = np.array([
        [point.x],
        [point.y],
        [point.z]
    ])

    result = H @ vec

    w = result[2, 0]

    if abs(w) < 1e-9:
        return PVector()

    return PVector(
        result[0, 0] / w,
        result[1, 0] / w,
        0.0,
    )


# ============================================================
# CORNER HELPERS
# ============================================================

def corners_detected(tag_manager):
    """
    Processing:

    boolean cornersDetected()
    """

    return (
        tag_manager.tags[
            cornersID[0]
        ].active
        and
        tag_manager.tags[
            cornersID[1]
        ].active
        and
        tag_manager.tags[
            cornersID[2]
        ].active
    )


def is_corner(marker_id):
    """
    Processing:

    boolean isCorner(int id)
    """

    return marker_id in (
        cornersID[0],
        cornersID[1],
        cornersID[2]
    )


# ============================================================
# PLANE REGISTRATION
# ============================================================

def register_plane_points():
    """
    Processing:

    registerPlanePoints()
    """

    planePoints[0] = srcPointsT[0].copy()
    planePoints[1] = srcPointsT[1].copy()
    planePoints[2] = srcPointsT[2].copy()


def register_plane_orientation(
    corner_points_r=None,
    tag_manager=None,
):
    """
    Об'єднання двох Processing-перевантажень:

    registerPlaneOrientation()
    registerPlaneOrientation(PVector[])
    """

    global global_rx
    global global_ry
    global global_rz

    if corner_points_r is not None:

        global_rx = (
            corner_points_r[0].x +
            corner_points_r[1].x +
            corner_points_r[2].x
        ) / 3.0

        global_ry = (
            corner_points_r[0].y +
            corner_points_r[1].y +
            corner_points_r[2].y
        ) / 3.0

        global_rz = (
            corner_points_r[0].z +
            corner_points_r[1].z +
            corner_points_r[2].z
        ) / 3.0

    elif tag_manager is not None:

        global_rx = (
            tag_manager.tags[cornersID[0]].rx +
            tag_manager.tags[cornersID[1]].rx +
            tag_manager.tags[cornersID[2]].rx
        ) / 3.0

        global_ry = (
            tag_manager.tags[cornersID[0]].ry +
            tag_manager.tags[cornersID[1]].ry +
            tag_manager.tags[cornersID[2]].ry
        ) / 3.0

        global_rz = (
            tag_manager.tags[cornersID[0]].rz +
            tag_manager.tags[cornersID[1]].rz +
            tag_manager.tags[cornersID[2]].rz
        ) / 3.0
        
# ============================================================
# VECTOR MATH
# ============================================================

def subtract(v1: PVector, v2: PVector) -> PVector:
    """
    Processing:
    subtract(v1,v2)
    """

    return PVector(
        v1.x - v2.x,
        v1.y - v2.y,
        v1.z - v2.z
    )


def cross(v1: PVector, v2: PVector) -> PVector:
    """
    Processing:
    cross(v1,v2)
    """

    return PVector(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )


def dot(v1: PVector, v2: PVector) -> float:
    """
    Processing:
    dot(v1,v2)
    """

    return (
        v1.x * v2.x +
        v1.y * v2.y +
        v1.z * v2.z
    )


# ============================================================
# PLANE DISTANCE
# ============================================================

def distance_point_to_plane(
    point: PVector,
    plane_points
) -> float:
    """
    Processing:
    distancePointToPlane()
    """

    normal = cross(
        subtract(
            plane_points[1],
            plane_points[0]
        ),
        subtract(
            plane_points[2],
            plane_points[0]
        )
    )

    d = -dot(
        normal,
        plane_points[0]
    )

    numerator = abs(
        dot(normal, point) + d
    )

    denominator = math.sqrt(
        normal.x * normal.x +
        normal.y * normal.y +
        normal.z * normal.z
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator


# ============================================================
# SCREEN TRANSFORM
# ============================================================

def img2screen(p: PVector) -> PVector:
    """
    Processing:
    img2screen()
    """

    return PVector(
        p.x * markerGridWidth
        + windowOffset.x
        + imageOffset.x
        + markerOffset.x,

        p.y * markerGridWidth
        + windowOffset.y
        + imageOffset.y
        + markerOffset.y
    )


# ============================================================
# DISTANCE / ANGLE
# ============================================================

def get_distance_between(
    p0: PVector,
    p1: PVector
) -> float:
    """
    Processing:
    getDistanceBetween()
    """

    return math.dist(
        (p0.x, p0.y),
        (p1.x, p1.y)
    )


def get_angle_between(
    p0: PVector,
    p1: PVector
) -> float:
    """
    Processing:
    getAngleBetween()
    """

    return math.atan2(
        p1.y - p0.y,
        p1.x - p0.x
    )


def get_centroid_between(
    p0: PVector,
    p1: PVector
) -> PVector:
    """
    Processing:
    getCentroidBetween()
    """

    return PVector(
        (p0.x + p1.x) * 0.5,
        (p0.y + p1.y) * 0.5,
        (p0.z + p1.z) * 0.5
    )


# ============================================================
# TAGGED OBJECT LOOKUP
# ============================================================

def which_to(
    marker_id: int,
    TO_IDS
) -> int:
    """
    Processing:
    whichTO()
    """

    for i, ids in enumerate(TO_IDS):

        if len(ids) > 0 and ids[0] == marker_id:
            return i

    return -1


# ============================================================
# UNIT CONVERSION
# ============================================================

def mm_to_px(mm: float) -> float:
    """
    Processing:
    mmToPx()
    """

    return (
        mm
        * (72.0 / 25.4)
        * tag2screenRatio
    )


# ============================================================
# ROTATION MATRICES
# ============================================================

def get_rotation_matrix(
    roll: float,
    pitch: float,
    yaw: float
) -> PMatrix3D:
    """
    Processing:
    getRotationMatrix()
    """

    mat = PMatrix3D()

    # ZYX order

    mat.rotateZ(yaw)
    mat.rotateY(pitch)
    mat.rotateX(roll)

    return mat


# ============================================================
# TILT COMPUTATION
# ============================================================

def get_tilt_angles(
    tilt2d: PVector,
    angle2d: float
) -> PVector:
    """
    Processing:
    getTiltAngles()
    """

    obj = PVector(
        global_rx,
        global_ry,
        global_rz
    )

    surf = PVector(
        tilt2d.x,
        tilt2d.y,
        angle2d
    )

    #
    # Rotation matrices
    #

    R_s = get_rotation_matrix(
        surf.x,
        surf.y,
        surf.z
    )

    R_o = get_rotation_matrix(
        obj.x,
        obj.y,
        obj.z
    )

    #
    # Relative rotation
    #

    R_s.transpose()

    R_rel = PMatrix3D()
    R_rel.set(R_s)
    R_rel.apply(R_o)

    #
    # Euler extraction
    #

    tilt_x = math.atan2(
        R_rel.m21,
        R_rel.m22
    )

    tilt_y = math.atan2(
        -R_rel.m20,
        math.sqrt(
            R_rel.m21 ** 2 +
            R_rel.m22 ** 2
        )
    )

    rel_roll = math.atan2(
        R_rel.m10,
        R_rel.m00
    )

    return PVector(
        tilt_x,
        -tilt_y,
        rel_roll
    )


# ============================================================
# PROCESSING ALIASES
# ============================================================

distancePointToPlane = distance_point_to_plane

getDistanceBetween = get_distance_between
getAngleBetween = get_angle_between
getCentroidBetween = get_centroid_between

whichTO = which_to

mmToPx = mm_to_px

getRotationMatrix = get_rotation_matrix
getTiltAngles = get_tilt_angles

