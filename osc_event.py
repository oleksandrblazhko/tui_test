from models.pvector import PVector
from tools import tm


def osc_event(address, *args):

    if address != "/marker":
        return

    id_ = int(args[0])

    tx = float(args[1])
    ty = float(args[2])
    tz = float(args[3])

    rx = float(args[4])
    ry = float(args[5])
    rz = float(args[6])

    p1x = float(args[7])
    p1y = float(args[8])

    p2x = float(args[9])
    p2y = float(args[10])

    p3x = float(args[11])
    p3y = float(args[12])

    p4x = float(args[13])
    p4y = float(args[14])

    corners = [
        PVector(p1x, p1y),
        PVector(p2x, p2y),
        PVector(p3x, p3y),
        PVector(p4x, p4y)
    ]

    tm.set(
        id_,
        tx,
        ty,
        tz,
        rx,
        ry,
        rz,
        corners
    )