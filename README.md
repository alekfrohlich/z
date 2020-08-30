
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

- add(name, points, color, faces?, bmatu?, bmatv?) (**)
- translate(name, sx, sy, sz)
- scale(name, factor)
- rotate(name, x_angle, y_angle, z_angle)
- info(name)
- paint(name, r, g, b)

(**) Parameters followed by ? are considered optional.
