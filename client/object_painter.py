"""This module provides a class to draw objects given a Cairo.Context and the
viewport's resolution.

Classes
-------
    ObjectPainter

"""

class ObjectPainter:
    """"""
    def __init__(self, cr: 'Cairo.Context', resolution: 'tuple'):
        self._cr = cr
        self._res = resolution

    def resolution_transform(self, point: 'tuple') -> 'tuple':
        """Rescale points from normalized coordinate system to resolution.

        Notes
        -----
            10 is added to both transformed coordinates to account for
            the clip region.

        """
        x_w, y_w = point
        x_vp = (x_w + 1) / (2) * self._res[0] + 10
        y_vp = (1 - (y_w + 1) / (2)) * self._res[1] + 10
        return (x_vp, y_vp)

    def paint_point(self, point: 'Point'):
        """Draw point."""
        p = self.resolution_transform(point.cached_points[0])
        self._cr.move_to(*p)
        self._cr.line_to(*p)
        self._cr.stroke()

    def paint_line(self, line: 'Line'):
        """Draw line."""
        p0, p1 = list(map(self.resolution_transform, line.cached_points))
        self._cr.move_to(*p0)
        self._cr.line_to(*p1)
        self._cr.stroke()

    def paint_polymesh(self, mesh: 'Mesh'):
        """Draw vertex-face mesh."""
        points = list(map(self.resolution_transform, mesh.cached_points))
        for face in mesh.cached_faces:
            self._cr.move_to(*points[face[0]])
            for i in face[1:]:
                self._cr.line_to(*points[i])
            self._cr.line_to(*points[face[0]])
            self._cr.stroke()

    def paint_curve(self, curve: 'Curve'):
        """Draw curve."""
        points = list(map(self.resolution_transform, curve.cached_points))
        self._cr.move_to(*points[0])
        for p in points:
            self._cr.line_to(*p)
        self._cr.stroke()
