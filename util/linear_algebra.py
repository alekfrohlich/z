"""Basic homogeneous coordinates utilities."""

import numpy as np


def translation_matrix(dx, dy, dz):
    """Parameterized translation matrix."""
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [dx, dy, dz, 1]])


def escalation_matrix(sx, sy, sz):
    """Parameterized escalation matrix."""
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def rotation_matrix(x_angle, y_angle, z_angle):
    """Parameterized rotation matrix."""
    return np.array(
                    [[1, 0, 0, 0],
                     [0, np.cos(x_angle), -np.sin(x_angle), 0],
                     [0, np.sin(x_angle), np.cos(x_angle), 0],
                     [0, 0, 0, 1]]
         )@np.array(
                    [[np.cos(y_angle), 0, np.sin(y_angle), 0],
                     [0, 1, 0, 0],
                     [-np.sin(y_angle), 0, np.cos(y_angle), 0],
                     [0, 0, 0, 1]]
         )@np.array(
                    [[np.cos(z_angle), -np.sin(z_angle), 0, 0],
                     [np.sin(z_angle), np.cos(z_angle), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def size(u):
    """Size of 3D vector."""
    return ((u[0][0] - u[1][0])**2 +
            (u[0][1] - u[1][1])**2 +
            (u[0][2] - u[1][2])**2)**0.5


def transformed(points, matrix_tr):
    """Vector after applying linear transformation."""
    return list(map(lambda p: np.dot(p, matrix_tr), points))
