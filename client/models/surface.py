import numpy as np
"""This module provides a Surface class."""
from .paintable_object import PaintableObject


class Surface(PaintableObject):
    """Surface given by control points in homogeneous coordinates."""

    def calculateCoefficients(self):
        # print("Cx:")
        self._Cx = self._bmatu@self._Ax@np.transpose(self._bmatu)
        # self._Cx = self._bmatu@self._Ax@self._bmatu
        # print(self._Cx)

        # print("Cy:")
        self._Cy = self._bmatu@self._Ay@np.transpose(self._bmatu)
        # self._Cy = self._bmatu@self._Ay@self._bmatu
        # print(self._Cy)

        # print("Cz:")
        # self._Cz = self._bmatu@self._Az@np.transpose(self._bmatu)
        # print(self._Cz)

    def createDeltaMatrices(self, delta_s, delta_t):
        # print("Es")
        self._Es = np.array([[0,0,0,1],
                             [delta_s * delta_s * delta_s, delta_s * delta_s, delta_s, 0],
                             [6 * delta_s * delta_s * delta_s, 2 * delta_s * delta_s, 0,0],
                             [6 * delta_s * delta_s * delta_s,0,0,0]
                            ])
        # print(self._Es)

        # print("Et")
        self._Et = np.transpose(
                    np.array([[0,0,0,1],
                             [delta_t * delta_t * delta_t, delta_t * delta_t, delta_t, 0 ],
                             [6 * delta_t * delta_t * delta_t, 2 * delta_t * delta_t, 0,0],
                             [6 * delta_t * delta_t * delta_t,0,0,0]
                            ])
                             )
        # print(self._Et)

    def createForwardDiffMatrices(self):
        # print("DDx")
        self._DDx = self._Es@self._Cx@self._Et
        # print(self._DDx)

        # print("DDy")
        self._DDy = self._Es@self._Cy@self._Et
        # print(self._DDy)

        # print("DDz")
        # self._DDz = self._Es@self._Cz@self._Et
        # print(self._DDz)

    # TODO: guardar pontos calculados
    # def DrawCurveFwdDif(self, n,\
    #                     x, Dx, D2x, D3x, \
    #                     y, Dy, D2y, D3y, \
    #                     z, Dz, D2z, D3z):
    #     oldx = x
    #     oldy = y
    #     oldz = z
    #     # stroke(#FFFFFF);
    #     for i in range (n-1):
    #         x = x + Dx;  Dx = Dx + D2x;  D2x = D2x + D3x
    #         y = y + Dy;  Dy = Dy + D2y;  D2y = D2y + D3y
    #         z = z + Dz;  Dz = Dz + D2z;  D2z = D2z + D3z
    #         # line((float)oldx, (float)oldy, (float)oldz, (float)x, (float)y, (float)z); // Draw line segment
    #         oldx = x
    #         oldy = y
    #         oldz = z

    def UpdateForwardDiffMatrices(self):
        # //row1 <- row1 + row2
        self._DDx[0][0] =  self._DDx[0][0]+self._DDx[1][0];  self._DDx[0][1] = self._DDx[0][1]+self._DDx[1][1]; self._DDx[0][2] = self._DDx[0][2]+self._DDx[1][2]; self._DDx[0][3] = self._DDx[0][3]+self._DDx[1][3]
        self._DDy[0][0] =  self._DDy[0][0]+self._DDy[1][0];  self._DDy[0][1] = self._DDy[0][1]+self._DDy[1][1]; self._DDy[0][2] = self._DDy[0][2]+self._DDy[1][2]; self._DDy[0][3] = self._DDy[0][3]+self._DDy[1][3]
        # self._DDz[0][0] =  self._DDz[0][    0]+self._DDz[1][0];  self._DDz[0][1] = self._DDz[0][1]+self._DDz[1][1]; self._DDz[0][2] = self._DDz[0][2]+self._DDz[1][2]; self._DDz[0][3] = self._DDz[0][3]+self._DDz[1][3]
        # //row2 <- row2 + row3
        self._DDx[1][0] =  self._DDx[1][0]+self._DDx[2][0]; self._DDx[1][1] = self._DDx[1][1]+self._DDx[2][1]; self._DDx[1][2] = self._DDx[1][2]+self._DDx[2][2]; self._DDx[1][3] = self._DDx[1][3]+self._DDx[2][3]
        self._DDy[1][0] =  self._DDy[1][0]+self._DDy[2][0]; self._DDy[1][1] = self._DDy[1][1]+self._DDy[2][1]; self._DDy[1][2] = self._DDy[1][2]+self._DDy[2][2]; self._DDy[1][3] = self._DDy[1][3]+self._DDy[2][3]
        # self._DDz[1][0] =  self._DDz[1][0]+self._DDz[2][0]; self._DDz[1][1] = self._DDz[1][1]+self._DDz[2][1]; self._DDz[1][2] = self._DDz[1][2]+self._DDz[2][2]; self._DDz[1][3] = self._DDz[1][3]+self._DDz[2][3]
        # //row3 <- row3 + row4
        self._DDx[2][0] =  self._DDx[2][0]+self._DDx[3][0]; self._DDx[2][1] = self._DDx[2][1]+self._DDx[3][1]; self._DDx[2][2] = self._DDx[2][2]+self._DDx[3][2]; self._DDx[2][3] = self._DDx[2][3]+self._DDx[3][3]
        self._DDy[2][0] =  self._DDy[2][0]+self._DDy[3][0]; self._DDy[2][1] = self._DDy[2][1]+self._DDy[3][1]; self._DDy[2][2] = self._DDy[2][2]+self._DDy[3][2]; self._DDy[2][3] = self._DDy[2][3]+self._DDy[3][3]
        # self._DDz[2][0] =  self._DDz[2][0]+self._DDz[3][0]; self._DDz[2][1] = self._DDz[2][1]+self._DDz[3][1]; self._DDz[2][2] = self._DDz[2][2]+self._DDz[3][2]; self._DDz[2][3] = self._DDz[2][3]+self._DDz[3][3]



    # def DrawSurfaceFwdDif(self, ns, nt):
    #     delta_s = 1.0 / (ns - 1)
    #     delta_t = 1.0 / (nt - 1)
    #     self.createDeltaMatrices(delta_s, delta_t)
    #     self.createForwardDiffMatrices()

    #     for i in range(ns):
    #         self.DrawCurveFwdDif(nt,
    #                  self._DDx[0][0], self._DDx[0][1], self._DDx[0][2], self._DDx[0][3],
    #                  self._DDy[0][0], self._DDy[0][1], self._DDy[0][2], self._DDy[0][3],
    #                  self._DDz[0][0], self._DDz[0][1], self._DDz[0][2], self._DDz[0][3] )
    #         self.UpdateForwardDiffMatrices()

    #     createForwardDiffMatrices()
    #     self._DDx = np.transpose(self._DDx)
    #     self._DDy = np.transpose(self._DDy)
    #     self._DDz = np.transpose(self._DDz)

    #     for i in range(nt):
    #         self.DrawCurveFwdDif(ns,
    #                  self._DDx[0][0], self._DDx[0][1], self._DDx[0][2], self._DDx[0][3],
    #                  self._DDy[0][0], self._DDy[0][1], self._DDy[0][2], self._DDy[0][3],
    #                  self._DDz[0][0], self._DDz[0][1], self._DDz[0][2], self._DDz[0][3] )
    #         self.UpdateForwardDiffMatrices()




    # def build_surface(self, control_points: 'list') -> 'list':
    #     ns = 15
    #     nt = 15
    #     self.calculateCoefficients()
    #     self.DrawSurfaceFwdDif(ns, nt)

    def createGeometryMatrix(self, control_points):
        # print("control_points")
        # print(control_points)
        # print("GeometryMatrix")
        # print("Ax")
        self._Ax = np.array([ [control_points[0][0], control_points[1][0], control_points[2][0], control_points[3][0]],
                        [control_points[4][0], control_points[5][0], control_points[6][0], control_points[7][0]],
                        [control_points[8][0], control_points[9][0], control_points[10][0], control_points[11][0]],
                        [control_points[12][0], control_points[13][0], control_points[14][0], control_points[15][0]],
                        ])
        # print(self._Ax)
        # print("Ay")
        self._Ay = np.array([ [control_points[0][1], control_points[1][1], control_points[2][1], control_points[3][1]],
                        [control_points[4][1], control_points[5][1], control_points[6][1], control_points[7][1]],
                        [control_points[8][1], control_points[9][1], control_points[10][1], control_points[11][1]],
                        [control_points[12][1], control_points[13][1], control_points[14][1], control_points[15][1]],
                        ])
        # print(self._Ay)
        # print("Az")
        # self._Az = np.array([ [control_points[0][2], control_points[1][2], control_points[2][2], control_points[3][2]],
        #                 [control_points[4][2], control_points[5][2], control_points[6][2], control_points[7][2]],
        #                 [control_points[8][2], control_points[9][2], control_points[10][2], control_points[11][2]],
        #                 [control_points[12][2], control_points[13][2], control_points[14][2], control_points[15][2]],
        #                 ])
        # # print(self._Az)

    def __init__(self, name: 'str', points: 'list', bmatu: 'ndarray',
                 bmatv: 'ndarray', color: 'tuple'):
        """Construct Surface."""

        self._bmatu = bmatu
        self._bmatv = bmatv
        # self.createGeometryMatrix(points)

        # super().__init__(name, self.build_surface(control_points), color, 0.5)
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
