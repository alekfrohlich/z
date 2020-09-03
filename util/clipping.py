"""This module provides 2D clipping algorithms.

Implemented algorithms:
- Point clipping
- Line clipping (Cohen-Sutherland)
- Polygon clipping (Sutherland-Hodgeman_
- Wireframe clipping

Notes
-----
    All algorithms are based on a normalized coordinate system where
    the borders of the window are at [(-1,1), (1,1), (1,-1), (-1,-1)].

    Curves are clipped whilst been drawn for optimization purposes.

"""


def clip_point(points: 'list') -> 'tuple':
    """Point clipping algorithm."""
    x, y = points[0]
    if x > 1 or x < -1 or y > 1 or y < -1:
        return []
    else:
        return points


def clip_line(points: 'list', xmax=1, xmin=-1, ymax=1, ymin=-1) -> 'list':
    """Cohen-Sutherland line clipping algorithm."""
    def region_code(x, y):
        code = 0
        if x < xmin:
            code += 1
        elif x > xmax:
            code += 2
        if y < ymin:
            code += 4
        elif y > ymax:
            code += 8
        return code

    def left_intersect(x, y):
        return (xmin, m * (xmin - x) + y)

    def up_intersect(x, y):
        return (x + 1/m * (ymax - y), ymax)

    def right_intersect(x, y):
        return (xmax, m * (xmax - x) + y)

    def down_intersect(x, y):
        return (x + 1/m * (ymin - y), ymin)

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
            if i[0] <= xmax and i[0] >= xmin and i[1] <= ymax and i[1] >= ymin:
                return (i[0], i[1])
        return []

    x1, y1 = points[0]
    x2, y2 = points[1]
    rc1 = region_code(x1, y1)
    rc2 = region_code(x2, y2)
    if rc1 == 0 and rc2 == 0:  # completely inside
        return points
    elif (rc1 & rc2) != 0:  # completely outside
        return []
    else:  # partially inside
        m = (y2-y1) / (x2-x1)
        if rc1 == 0 or rc2 == 0:  # one intersection
            if rc1 != 0:
                i = valid_intersection(intersections(x1, y1, rc1))
                return [i, (x2, y2)]
            else:
                i = valid_intersection(intersections(x2, y2, rc2))
                return [i, (x1, y1)]
        else:  # possibly two intersections
            i1 = valid_intersection(intersections(x1, y1, rc1))
            i2 = valid_intersection(intersections(x2, y2, rc2))
            if i1 == [] or i2 == []:  # outside
                return []
            return [i1, i2]


def clip_polygon(points: 'list') -> 'list':
    """Sutherland-Hodgeman polygon clipping algortihm."""
    def intersect(p1, p2, xw, yw):
        """Intersection between line and window border."""
        x1, y1 = p1
        x2, y2 = p2

        if x1-x2 != 0:
            m = (y1-y2) / (x1-x2)
            b = y1 - m*x1

            if yw is not None:
                xw = (yw-b)/m
            else:
                yw = m*xw + b
        else:
            if yw is not None:
                xw = x1
            else:
                pass
        return (xw, yw)

    def out(point):
        """Test if point is outside current border."""
        if border == 0:
            return point[0] < -1
        elif border == 1:
            return point[1] > 1
        elif border == 2:
            return point[0] > 1
        else:
            return point[1] < -1

    xw = [-1.0, None, 1.0, None]
    yw = [None, 1.0, None, -1.0]

    old_points = points
    new_points = []

    for border in range(4):
        for i in range(len(old_points)):
            j = (i + 1) % len(old_points)
            pi = old_points[i]
            pj = old_points[j]
            if out(pi) and out(pj):
                continue
            elif not out(pi) and out(pj):
                new_points.append(intersect(pi, pj, xw[border], yw[border]))
            elif out(pi) and not out(pj):
                new_points.append(intersect(pi, pj, xw[border], yw[border]))
                new_points.append(pj)
            else:
                new_points.append(pj)
        if len(new_points) != 0:
            new_points.append(new_points[0])
        old_points = new_points[:]
        new_points = []
    return old_points


def clip_wireframe(points: 'list', faces: 'list') -> 'tuple':
    """Clip wireframe by polygon clipping each of it's faces.

    Notes
    -----
        The method `index` of `list` runs in O(n) time. `clip_wireframe` could
        be optimized if an ordered set was used instead of list.

    """
    def try_add(point: 'tuple') -> 'int':
        """Add point to `new_points` and return index to it.

        Notes
        -----
            If `point` is already on `new_points`, don't repeat point. Instead,
            return index to existing point.
        """
        try:
            index = new_points.index(point)
        except ValueError:
            new_points.append(point)
            index = len(new_points) - 1
        return index

    new_points = []
    new_faces = []
    for face in faces:
        clipped_points = clip_polygon([points[i] for i in face])
        if clipped_points:
            new_faces.append([try_add(p) for p in clipped_points])
    return (new_points, new_faces)
