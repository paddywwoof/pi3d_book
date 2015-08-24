#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

display = pi3d.Display.create(w=800, h=600, frames_per_second=15, samples=4)

vertices = [[-2.0, -1.0, 0.0], [0.0, 3.0, 3.0], [4.0, -2.0, 1.0], [0.0, -2.0, 4.0]]
indices = [[0, 1, 2], [0, 3, 1], [2, 1, 3], [0, 2, 3]]
""" So with four vertices it should be possible to make a tetrahedron.
Note that all the faces have to be defined in anticlockwise order for
each face.

Run it first of all as it is. You will see the effect of normals. So far
we have allowed the Buffer to work out the direction of the normals - by
not sending any. The normal vectors are worked out at each vertex by
taking the cross products of the edges then averaged. The result is 'smooth'
which is great for spheres, say, but not wanted for a tetrahedron.

The only way to fix this is to have independent vertices at each corner
of the tetrahedron, one for each face that meets there. i.e. there need to
be 12 rather than 4 vertices.

Uncomment the two alternative lines below to see the difference.

You will realise that it is becoming almost impossible to keep track of
which vertex belongs with which face... Time to start getting python to
do the work for us.
"""

#vertices = [[-2.0, -1.0, 0.0], [-2.0, -1.0, 0.0], [-2.0, -1.0, 0.0],
#            [0.0, 3.0, 3.0],   [0.0, 3.0, 3.0],   [0.0, 3.0, 3.0],
#            [4.0, -2.0, 1.0],  [4.0, -2.0, 1.0],  [4.0, -2.0, 1.0],
#            [0.0, -2.0, 4.0],  [0.0, -2.0, 4.0],  [0.0, -2.0, 4.0]]
#indices = [[0, 3, 6], [1, 9, 4], [7, 5, 10], [2, 8, 11]]

triangle = pi3d.Shape(None, None, None, 0.0, 0.0, 10.0,  0.0, 0.0, 0.0,
                                        1.0, 1.0, 1.0,   0.0, 0.0, 0.0) 
triangle.buf = [pi3d.Buffer(triangle, pts=vertices, texcoords=[], faces=indices)]

while display.loop_running():
  triangle.draw()
  triangle.rotateIncY(1.0)
  triangle.rotateIncZ(2.631)
  triangle.rotateIncX(0.23)
