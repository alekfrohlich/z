""" A fraction of World. """

import numpy as np

from core.log import Logger, LogLevel


def cohen_sutherland(points):
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
        return (-1, m * (1 - x) + y)

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
            9:  [left_intersect, up_intersect],
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
    print(points)
    print((rc1, rc2))
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
                i = valid_intersection(intesections(x2, y2, rc2))
                return (i, np.array([x1, y1, 1]))
        else: # possibly two intersections
            int1 = valid_intersection(intersections(x1, y1, rc1))
            int2 = valid_intersection(intersections(x2, y2, rc2))
            if int1 is None or int2 is None: # outside
                return None
            return (int1, int2)
            # corner case


class Window:
    def __init__(self):
        self.points = [
            np.array([0, 500, 1]),
            np.array([500, 500, 1]),
            np.array([500, 0, 1]),
            np.array([0, 0, 1])]
        self.angle = 0

    @property
    def center(self):
        x_points = [point[0] for point in self.points]
        y_points = [point[1] for point in self.points]
        return (np.average(x_points), np.average(y_points))

    def clip(self, points, obj_type):
        def clip_point(points):
            x, y, _ = points[0]
            if x > 1 or x < -1 or y > 1 or y < -1:
                return None
            else:
                return points

        def clip_line(points):
            return cohen_sutherland(points)

        def clip_wireframe(points):
            return points

        obj_t2func = {
            1: clip_point,
            2: clip_line,
            3: clip_wireframe,
        }
        return obj_t2func[obj_type.value](points)


    def translate(self, dx, dy):
        """ Translates object by (dx, dy). """
        translate_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [dx, dy, 1]])
        self.transform(translate_tr)

    def scale(self, sx, sy):
        """ Scales object by sx in the x coordinate and sy in the
            y coordinate. """
        x_center, y_center = self.center

        to_origin_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [-x_center, -y_center, 1]])

        scale_tr = np.array([[sx, 0, 0],
                             [0, sy, 0],
                             [0, 0, 1]])

        from_origin_tr = np.array([[1, 0, 0],
                                   [0, 1, 0],
                                   [x_center, y_center, 1]])

        concat_tr = to_origin_tr.dot(scale_tr.dot(from_origin_tr))
        self.transform(concat_tr)

    def rotate(self, degrees, point=None):
        """ Rotates object by 'degrees' in respect to a point. """
        if point is None:
            point = self.center
        x, y = point

        to_origin_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [-x, -y, 1]])

        rotate_tr = np.array([[np.cos(degrees), -np.sin(degrees), 0],
                             [np.sin(degrees), np.cos(degrees), 0],
                             [0, 0, 1]])

        from_origin_tr = np.array([[1, 0, 0],
                                   [0, 1, 0],
                                   [x, y, 1]])
        concat_tr = to_origin_tr.dot(rotate_tr.dot(from_origin_tr))
        self.transform(concat_tr)
        self.angle = (self.angle + degrees) % 360

    def transform(self, matrix_tr):
        """ Applies transformation matrix to each of the object's
            coordinates. """
        for i in range(len(self.points)):
            self.points[i] = self.points[i].dot(matrix_tr)

    def window_transform(self, points):
        x, y = self.center

        to_origin_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [-x, -y, 1]])

        rotate_tr = np.array([[np.cos(self.angle), -np.sin(self.angle), 0],
                              [np.sin(self.angle), np.cos(self.angle), 0],
                              [0, 0, 1]])

        vup = ((self.points[0][0] - self.points[3][0])**2 + (self.points[0][1] - self.points[3][1])**2)**0.5
        vright = ((self.points[2][0] - self.points[3][0])**2 + (self.points[2][1] - self.points[3][1])**2)**0.5

        scale_tr = np.array([[2/vup, 0, 0],
                             [0, 2/vright, 0],
                             [0, 0, 1]])

        concat_tr = to_origin_tr.dot(rotate_tr.dot(scale_tr))

        new_points = []
        for i in range(len(points)):
            new_points.append(points[i].dot(concat_tr))
        return new_points
