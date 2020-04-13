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


def translation_matrix(dx, dy):
    return np.array([[1, 0, 0],
                     [0, 1, 0],
                     [dx, dy, 1]])


def escalation_matrix(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])


def rotation_matrix(rads):
    return np.array([[np.cos(rads), np.sin(rads), 0],
                     [-np.sin(rads), np.cos(rads), 0],
                     [0, 0, 1]])


def normalize_matrix(u, v):
    return escalation_matrix(2/size(u), 2/size(v))


# UTIL
def normal(p0, p1):
    # clockwise!
    # not unitary
    return (p0[1] - p1[1], p1[0] - p0[0])


def size(u):
    return ((u[0][0] - u[1][0])**2 +
            (u[0][1] - u[1][1])**2)**0.5


def affine_transformed(p, points, matrix_tr):
    affine_tr = translation_matrix(-p[0], -p[1])@matrix_tr
    new_points = []
    for i in range(len(points)):
        new_points.append(points[i]@affine_tr)
    return new_points
