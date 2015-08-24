#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

display = pi3d.Display.create(w=800, h=600, frames_per_second=10)

""" vertices for triangle 0,1,2 i.e [[0x,0y,0z], [1x,1y,1z], [2x,2y,2z]]
"""
vertices = [[-2.0, -1.0, 0.0], [0.0, 3.0, 0.0], [4.0, -2.0, 0.0]]
indices = [[0, 1, 2]]

""" The Shape object hold general info to pass to the gpu about position,
orientation etc. These are used to make the translation and projection matrices
"""
triangle = pi3d.Shape(None, None, None,      # camera, light, name (see note below)
                      0.0, 0.0, 10.0,        # x,y,z
                      0.0, 0.0, 0.0,         # rotation about x,y,z axes
                      1.0, 1.0, 1.0,         # scale in x,y,z directions
                      0.0, 0.0, 0.0)         # offset (i.e. for rotation) in x,y,z

""" Shapes have a list of Buffer objects that hold arrays of coordinates
for rendering
"""
triangle.buf = [pi3d.Buffer(triangle,        # pointer to the 'parent' Shape
                            pts=vertices,    # array of n x 3 coordinates
                            texcoords=[],    # array of n x 2 texture mapping coordinates
                            faces=indices)]  # array of m x 3 corner vertices

while display.loop_running():
  triangle.draw()
""" When draw() is called it checks to see if a Light, Camera and Shader
have been defined otherwise default ones are created.

NB: notice that the z location of the triangle has been set to 10.0, try
altering this figure i.e. reduce it to 0.0 in stages.

Also try adjusting the x,y,z positions of the vertices.

What happens if you "turn it round" so the sequence of vertices go round
the triangle anti-clockwise. Try changing the x and y locations then try
changing the order in the indices list.
"""
