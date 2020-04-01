import numpy as np

# TODO: Unify all clipping algorithms under a clipping.py module.

def cohen_sutherland(points):
    # print("============================")
    # print(points)
    """ Cohen-Sutherland line clipping algorithm based on a normalized
        coordinate system. """
    def region_code(x, y):
        code = 0
        if x < -1:
            code += 1
        elif x > 1:
            code += 2
        if y < -1:
            code += 4
        elif y > 1:
            code += 8
        return code

    def left_intersect(x, y):
        return (-1, m * (-1 - x) + y)

    def up_intersect(x, y):
        return (x + 1/m * (1 - y), 1)

    def right_intersect(x, y):
        return (1, m * (1 - x) + y)

    def down_intersect(x, y):
        return (x + 1/m * (-1 - y), -1)

    def intersections(x, y, code):
        rc2int = {
            1: [left_intersect],
            2: [right_intersect],
            4: [down_intersect],
            5: [left_intersect, down_intersect],
            6: [right_intersect, down_intersect],
            8: [up_intersect],
            9: [left_intersect, up_intersect],
            10: [right_intersect, up_intersect],
        }
        return [i(x, y) for i in rc2int[code]]

    def valid_intersection(intersections):
        for i in intersections:
            if i[0] <= 1 and i[0] >= -1 and i[1] <= 1 and i[1] >= -1:
                return np.array([i[0], i[1], 1])
        return None

    x1, y1, _ = points[0]
    x2, y2, _ = points[1]
    rc1 = region_code(x1, y1)
    rc2 = region_code(x2, y2)
    if rc1 == 0 and rc2 == 0: # completely inside
        return points
    elif (rc1 & rc2) != 0: # completely outside
        return None
    else: # partially inside
        m = (y2-y1) / (x2-x1)
        if rc1 == 0 or rc2 == 0: # one intersection
            if rc1 != 0:
                i = valid_intersection(intersections(x1, y1, rc1))
                return (i, np.array([x2, y2, 1]))
            else:
                i = valid_intersection(intersections(x2, y2, rc2))
                return (i, np.array([x1, y1, 1]))
        else: # possibly two intersections
            i1 = valid_intersection(intersections(x1, y1, rc1))
            i2 = valid_intersection(intersections(x2, y2, rc2))
            if i1 is None or i2 is None: # outside
                return None
            return (i1, i2)
