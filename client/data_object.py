"""
data_object.py

Port of DataObject.pde

ArUco-TUI Client v26.1
"""

from dataclasses import dataclass, field

from tools import PVector


@dataclass
class DataObject:

    dataID: int
    multiControl: bool
    val: float

    x: float
    y: float

    w: float
    h: float

    name: str

    rx: float = 0.0
    ry: float = 0.0
    rz: float = 0.0

    lastCtrlID: int = -1

    tempVal: float = 0.0

    ctrlIDList: list = field(default_factory=list)

    ref2DList: list = field(default_factory=list)

    ref_rList: list = field(default_factory=list)

    ref2D: PVector = field(
        default_factory=lambda: PVector(0, 0)
    )

    ref_r: float = 0.0

    bEngaged: bool = False

    d0: float = 0.0

    theta0: float = 0.0

    theta_p: float = 0.0

    m0: PVector = field(
        default_factory=lambda: PVector(0, 0)
    )

    gestureType: int = 0

    numTouches: int = 0

    gesturePerformed: bool = False

    scale: float = 1.0

    rotation: float = 0.0

    prev_rotation: float = 0.0

    translation: PVector = field(
        default_factory=lambda: PVector(0, 0)
    )

    lastGestureInfo: str = ""

    UNDEFINED = 0

    # --------------------------------------------------
    # values
    # --------------------------------------------------

    def set_value(self, value):

        self.val = value

    def set_temp_val(self, value):

        self.tempVal = value

    # --------------------------------------------------
    # control ids
    # --------------------------------------------------

    def add_ctrl_id(
            self,
            ctrl_id,
            ref2d,
            ref_r):

        self.ctrlIDList.append(ctrl_id)

        self.ref2DList.append(ref2d)

        self.ref_rList.append(ref_r)

    def remove_ctrl_id(
            self,
            ctrl_id):

        for i in range(
                len(self.ctrlIDList) - 1,
                -1,
                -1):

            if self.ctrlIDList[i] == ctrl_id:

                self.ctrlIDList.pop(i)

                self.ref2DList.pop(i)

                self.ref_rList.pop(i)

    def has_ctrl_id(
            self,
            ctrl_id):

        return ctrl_id in self.ctrlIDList

    def get_ctrl_counts(self):

        return len(self.ctrlIDList)

    # --------------------------------------------------
    # rotation
    # --------------------------------------------------

    def set_previous_rotation(
            self,
            rotation):

        self.prev_rotation = rotation

    # --------------------------------------------------
    # references
    # --------------------------------------------------

    def set_ref2d(
            self,
            point,
            rotation):

        self.ref2D = PVector(
            point.x,
            point.y
        )

        self.ref_r = rotation

    # --------------------------------------------------
    # updates
    # --------------------------------------------------

    def update_loc2d(
            self,
            x,
            y):

        self.x = x
        self.y = y

    def update_ori2d(
            self,
            rz):

        self.rz = rz

    def update_ori3d(
            self,
            rx,
            ry,
            rz):

        self.rx = rx
        self.ry = ry
        self.rz = rz

    # --------------------------------------------------
    # hit test
    # --------------------------------------------------

    def check_hit(
            self,
            cx,
            cy,
            d=0):

        return (
            abs(self.x - cx) < self.w / 2
            and
            abs(self.y - cy) < self.h / 2
        )

    # --------------------------------------------------
    # gestures
    # --------------------------------------------------

    def get_st_gesture_type(self):

        pass

    def draw_st_gesture_type(self):

        pass

    def draw_st_gesture_info(self):

        pass
        
        