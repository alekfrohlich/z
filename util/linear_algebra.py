# FIXME: Major modelling decisions need to be made before I bother documenting
#        this module.

# QUESTION: How to define translations? Linear transformations do not change
#           the origin, so we need some other way to formalize translations.
#           On the one hand, one could use the theory of affine spaces and
#           define translations as affine transformations with the associated
#           identity linear transformation but I dont know how to integrate
#           this vision with homogeneous coordinates. On the other hand, one
#           could define as mappings from different vector spaces (visulization
#           vs workbench) and keep relying on the computational hack to arrive
#           at the same affine coordinates.

# QUESTION: How to avoid gimbal locks? It seems that Aldo is going to teach us
#           Euler angles and that is susceptible to gimbal lock. We could use
#           Quartenions but I know nothing about them.


import numpy as np


def translation_matrix(dx, dy, dz):
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [dx, dy, dz, 1]])


def escalation_matrix(sx, sy, sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def rotation_matrix(x_angle, y_angle, z_angle):
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


def normalize_matrix(u, v):
    # TEMP: z scale fator o 1?
    return escalation_matrix(2/size(u), 2/size(v), 1)


def normal(p0, p1):
    # clockwise!
    # not unitary
    # TEMP: not 3d
    return (p0[1] - p1[1], p1[0] - p0[0])


def size(u):
    # TEMP: not 3d
    return ((u[0][0] - u[1][0])**2 +
            (u[0][1] - u[1][1])**2)**0.5


def affine_transformed(p, points, matrix_tr):
    affine_tr = translation_matrix(-p[0], -p[1], -p[2])@matrix_tr
    new_points = []
    for i in range(len(points)):
        new_points.append(points[i]@affine_tr)
    return new_points
