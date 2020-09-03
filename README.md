
 Z - Interactive Graphics System

## What is it?

Z is an interactive graphics system that renders scenes described in .obj format.
It does not implement the whole thing, but should ignore features that it does not
support. The system also supports the creation of objects: points, lines, wireframes
(*), curves, and surfaces. Every object may be translated, scaled, and rotated.

(*) Loaded .obj scenes are treated as wireframe models.

## Dependencies

Z relies on Gtk-3.0, cairo, numpy and scipy.

## Running

To run Z, simpy type:

```
$ chmod +x z
$ ./z
```

## Using it

The user may choose to interact with the system by the graphical user interface or
through a console prompt. The console implements a simple, regular language called
Object Manipulation Langue (.oml). The commands are:

- add(name, points, faces?, bmatu?, bmatv?, color?) (**)
- translate(name, sx, sy, sz)
- scale(name, factor)
- rotate(name, x_angle, y_angle, z_angle)

To specify the object type you're adding, add the suffix (p|l|w|c|s) for point,
line, wireframe, curve, and surface; e.g., addp(p1,250,250,0).

(**) Parameters followed by ? are optional. Also, some are dependent on the object
    being created: faces is required for wireframe, bmatu for curves and surfaces,
    and bmatv for surfaces.