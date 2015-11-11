#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

display = pi3d.Display.create(x=50, y=50, w=800, h=600)

CAMERA = pi3d.Camera(is_3d=True)
shader = pi3d.Shader("uv_light")
#shader = pi3d.Shader("uv_flat")

cube = pi3d.Cuboid(camera=CAMERA, w=200, h=200, d=200, z=500.0)
tex = pi3d.Texture("techy1.jpg")
cube.set_draw_details(shader, [tex])
""" This code is effectively the same as 3D_matrices03.py, with the axes
and corner numbers removed but also using a texture sampler.

The other changes required are:

  creating a Texture instance from an image file.

  use of a uv mapping shader, the on most similar to mat_light is uv_light
  but try swapping to uv_flat to see the difference.

  using set_draw_details() instead of set_material() and set_shader().
  (Have a look in pi3d/Shape.py to see what these different methods do.)
  The Textures used by the Buffer objects of Shape are held as a list and,
  as in the next example (textures02.py) there can be up to three.
"""

keys = pi3d.Keyboard()
while display.loop_running():
  cube.draw()

  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # up
      cube.translateY(5.0)
    elif k == ord('s'): # down
      cube.translateY(-5.0)
    elif k == ord('a'): # left
      cube.translateX(-5.0)
    elif k == ord('d'): # right
      cube.translateX(5.0)
    elif k == ord('z'): # clockwise z
      cube.rotateIncZ(-2.5)
    elif k == ord('x'): # anti-clockwise z
      cube.rotateIncZ(2.5)
    elif k == ord('c'): # clockwise x
      cube.rotateIncX(-2.5)
    elif k == ord('v'): # anti-clockwise x
      cube.rotateIncX(2.5)
    elif k == ord('b'): # clockwise y
      cube.rotateIncY(-2.5)
    elif k == ord('n'): # anti-clockwise y
      cube.rotateIncY(2.5)

keys.close()
display.destroy()
