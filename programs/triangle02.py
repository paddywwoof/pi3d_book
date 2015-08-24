#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

""" There is an option to get the egl rendering to do anti-alias rendering
of the diagonal edges. This is done by setting the samples argument to 4 when
the Display is created. Windows implementations of OpenGLES functionality
can't cope with this for some reason so you will have to take it out if
you're using that (or set to 0)
"""
display = pi3d.Display.create(w=800, h=600, frames_per_second=15, samples=4)

""" This time make two different sets of vertices. As each is just one
triangle still we can re-use the indices list
"""
vertices1 = [[-2.0, -1.0, 0.0], [0.0, 3.0, 3.0], [4.0, -2.0, 1.0]]
vertices2 = [[1.0, -2.0, 2.0], [3.0, 3.0, 0.0], [6.0, -3.0, 2.0]]
indices = [[0, 1, 2]]

triangle = pi3d.Shape(None, None, None, 0.0, 0.0, 10.0,  0.0, 0.0, 0.0,
                                        1.0, 1.0, 1.0,   0.0, 0.0, 0.0) 
""" and create two Buffer objects
"""
triangle.buf = [pi3d.Buffer(triangle, pts=vertices1, texcoords=[], faces=indices),
                pi3d.Buffer(triangle, pts=vertices2, texcoords=[], faces=indices)]

""" and now set them to be different materials RGB. This method simply sets
the values as part of a larger array that gets sent to the gpu each time
the Buffer is drawn. i.e. you can change the material from frame to frame.
"""
triangle.buf[0].set_material((1.0, 0.0, 0.5))
triangle.buf[1].set_material((0.0, 1.0, 0.5))

while display.loop_running():
  triangle.draw()
  """ To see the effect of directional lighting rotate the triangle around
  the y (vertical) axis by uncommenting the line below. Notice what happens
  when you look at the back of the triangle. The method takes an angle in degrees.
  """
  triangle.rotateIncY(1.0)
  """ Try increasing the frame rate up at the top where the Display is
  created.

  Then put it back to something low, change the rotation to 30.0 degrees
  and uncomment the line below to print 0:the model transformation and
  1:the projection matrix.

  The model transformation matrix is used for lighting and the projection
  matrix is used to 'flatten' the 3D space to 2D screen coordinates. Notice
  how the gpu keeps track of what is in front of what.
  """
  print("model:\n{}\nprojection:\n{}\n\n".format(triangle.M[0], triangle.M[1]))
