#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

display = pi3d.Display.create(w=800, h=600, frames_per_second=15, samples=4)

vertices1 = [[-2.0, -1.0, 0.0], [0.0, 3.0, 3.0], [4.0, -2.0, 1.0]]
vertices2 = [[1.0, -2.0, 2.0], [3.0, 3.0, 0.0], [6.0, -3.0, 2.0]]
""" As a quick aside, it's possible to tell the gpu to use the vertices
as ends of lines or simply as points. For lines to form a complete
triangle we need to carry on for more vertices as the mode used by pi3d doesn't
default to adding the last leg
"""
indices = [[0, 1, 2], [0, 1, 2]]

triangle = pi3d.Shape(None, None, None, 0.0, 0.0, 10.0,  0.0, 0.0, 0.0,
                                        1.0, 1.0, 1.0,   0.0, 0.0, 0.0) 
triangle.buf = [pi3d.Buffer(triangle, pts=vertices1, texcoords=[], faces=indices),
                pi3d.Buffer(triangle, pts=vertices2, texcoords=[], faces=indices)]


triangle.buf[0].set_material((1.0, 0.0, 0.5))
triangle.buf[1].set_material((0.0, 1.0, 0.5))
""" The default Shader uses directional lighting which has a rather odd
effect with lines and points. Normally you would use a 'flat' shader -
more on that later.

Try uncommenting each option. These Shape methods set a variable to be used
as the point size (which gets smaller with distance) or line width (which
is always the same, use a 3D object if you want perspective lines!). They
also set a variable used in the glDrawElements function to either GL_POINTS,
GL_LINE_STRIP as opposed to the default GL_TRIANGLES
"""
triangle.set_line_width(5)
#triangle.set_point_size(200)

while display.loop_running():
  triangle.draw()
  triangle.rotateIncY(1.0)
