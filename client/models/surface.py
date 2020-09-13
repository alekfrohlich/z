import numpy as np
"""This module provides a Surface class."""
from .paintable_object import PaintableObject


class Surface(PaintableObject):
    """Surface given by control points in homogeneous coordinates."""

    # def calculateCoefficients(self):
    #     # print("Cx:")
    #     self._Cx = self._bmatu@self._Ax@np.transpose(self._bmatu)
    #     # print(self._Cx)

    #     # print("Cy:")
    #     self._Cy = self._bmatu@self._Ay@np.transpose(self._bmatu)
    #     # print(self._Cy)

    # def createDeltaMatrices(self, delta):
    #     # print("Es")
    #     self._Es = np.array([[0,0,0,1],
    #                          [delta * delta * delta, delta * delta, delta, 0],
    #                          [6 * delta * delta * delta, 2 * delta * delta, 0,0],
    #                          [6 * delta * delta * delta,0,0,0]
    #                         ])
    #     # print(self._Es)

    #     # print("Et")
    #     self._Et = np.transpose((self._Es))
    #     # print(self._Et)

    # def createForwardDiffMatrices(self):
    #     # print("DDx")
    #     self._DDx = self._Es@self._Cx@self._Et
    #     # print(self._DDx)

    #     # print("DDy")
    #     self._DDy = self._Es@self._Cy@self._Et
    #     # print(self._DDy)

    # def UpdateForwardDiffMatrices(self):
    #     # row1 <- row1 + row2
    #     self._DDx[0,:] = self._DDx[0,:] + self._DDx[1,:]
    #     self._DDy[0,:] = self._DDy[0,:] + self._DDy[1,:]
    #     # row2 <- row2 + row3
    #     self._DDx[1,:] = self._DDx[1,:] + self._DDx[2,:]
    #     self._DDy[1,:] = self._DDy[1,:] + self._DDy[2,:]
    #     # row3 <- row3 + row4
    #     self._DDx[2,:] = self._DDx[2,:] + self._DDx[3,:]
    #     self._DDy[2,:] = self._DDy[2,:] + self._DDy[3,:]

    # def createGeometryMatrix(self, control_points):
    #     self._Ax = np.array([[control_points[i+4*j][0] for i in range(4)] for j in range(4)])
    #     self._Ay = np.array([[control_points[i+4*j][1] for i in range(4)] for j in range(4)])

    def __init__(self, name: 'str', points: 'list', bmatu: 'ndarray',
                 bmatv: 'ndarray', color: 'tuple'):
        """Construct Surface."""

        self._bmatu = bmatu
        self._bmatv = bmatv

        super().__init__(name, points, color, 0.5)

    def __str__(self):
        """Cohersion to string."""
        return "{}(Surface) with control points = {} and color = {}".format(
            self.name,
            str([(p[0], p[1], p[2]) for p in self._points]),
            str(self.color))

    @property
    def bmatu(self) -> 'Interpolator':
        """interpolator for the family of curves in u."""
        return self._bmatu

    @property
    def bmatv(self) -> 'Interpolator':
        """interpolator for the family of curves in v."""
        return self._bmatv

    @property
    def degu(self) -> 'int':
        """Degree of interpolator of family of curves in u."""
        return self._bmatu.shape[0] - 1

    @property
    def degv(self) -> 'int':
        """Degree of interpolator of family of curves in v."""
        return self._bmatv.shape[0] - 1


    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_surface(self)


    def update(self, window: 'Window'):
        """Generate visible parts of curve."""
        self._cached_points = self.projected(window)
