def osc_event(address, *args):

    if address == "/marker":

        id = int(args[0])

        tx = float(args[1])
        ty = float(args[2])
        tz = float(args[3])

        rx = float(args[4])
        ry = float(args[5])
        rz = float(args[6])

        corners = [
            PVector(args[7], args[8]),
            PVector(args[9], args[10]),
            PVector(args[11], args[12]),
            PVector(args[13], args[14]),
        ]

        tm.set(
            id,
            tx, ty, tz,
            rx, ry, rz,
            corners
        )
        
        
        