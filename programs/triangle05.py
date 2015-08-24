#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

display = pi3d.Display.create(w=800, h=600, frames_per_second=60, samples=4)

""" But first, just for fun, here's a two-tone tetrahedron
"""

vertices1 = [[-2.0, -1.0, 0.0], [-2.0, -1.0, 0.0],
            [0.0, 3.0, 3.0],    [0.0, 3.0, 3.0],
            [4.0, -2.0, 1.0],  
            [0.0, -2.0, 4.0]]
indices1 = [[0, 2, 4], [1, 5, 3]]

vertices2 = [[-2.0, -1.0, 0.0],
            [0.0, 3.0, 3.0],
            [4.0, -2.0, 1.0],  [4.0, -2.0, 1.0],
            [0.0, -2.0, 4.0],  [0.0, -2.0, 4.0]]
indices2 = [[2, 1, 4], [0, 3, 5]]

triangle = pi3d.Shape(None, None, None, 0.0, 0.0, 10.0,  0.0, 0.0, 0.0,
                                        1.0, 1.0, 1.0,   0.0, 0.0, 0.0) 
triangle.buf = [pi3d.Buffer(triangle, pts=vertices1, texcoords=[], faces=indices1),
                pi3d.Buffer(triangle, pts=vertices2, texcoords=[], faces=indices2)]

triangle.buf[0].set_material((0.85, 0.6, 0.05))
triangle.buf[1].set_material((0.02, 0.4, 0.6))

while display.loop_running():
  triangle.draw()
  triangle.rotateIncY(0.1)
  triangle.rotateIncZ(0.263)
  triangle.rotateIncX(0.023)
