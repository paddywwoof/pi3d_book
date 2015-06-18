#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

display = pi3d.Display.create(w=800, h=600)

CAMERA = pi3d.Camera(is_3d=True)
shader = pi3d.Shader("uv_reflect")
#shader = pi3d.Shader("uv_bump")
#shader = pi3d.Shader("uv_light")
#shader = pi3d.Shader("uv_flat")

cube = pi3d.Cuboid(camera=CAMERA, w=2.0, h=2.0, d=2.0, z=5.0)
tex = pi3d.Texture("techy1.jpg")
bump = pi3d.Texture("rocktile2.jpg")
refl = pi3d.Texture("glassbuilding.jpg")
cube.set_draw_details(shader, [tex, bump, refl], 2.0, 0.2, 2.0, 2.0)
""" Following from textures01.py this demo includes three textures. The
self color one ``tex``, as before, plus a normal or bump map ``bump`` and
a reflection image ``refl``.

In order to use all three the cube has to be given the uv_reflect shader
and the textures are passed as a list in set_draw_details(). Note also that
this method has extra arguments to control the repeat tiling of the normal
map image, the amount of reflection to show and the u and v tiling multiplication
factors. If you had a look at the method in pi3d/Shape.py you will already
know what they do. Try changing all these values and see what effect
they have.

The cube is also smaller and nearer to the view point. This is because the
effect of surface detail decreases with distance and at 500 units away
would be invisible. Try adding some zeros again and see what effect distance
has on normal mapping - especially with reflection levels > 0.5 and distances
around 500 to 600. Try moving the cube to 1500 units from the Camera and
making it 1000x1000x1000 (hint, rotate it with b and n keys) in pi3d/Display.py
you will see that ``DEFAULT_FAR = 1000.0``, sometimes you need to increase this
either when you create() the Display or a Camera.

Finally the w,a,s,d keys now change the texture tiling parameters rather
than moving the cube vertically and horizontally.
"""
u_off, v_off = 0.0, 0.0
keys = pi3d.Keyboard()
while display.loop_running():
  cube.draw()

  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # up
      v_off += 0.02
    elif k == ord('s'): # down
      v_off -= 0.02
    elif k == ord('a'): # left
      u_off -= 0.02
    elif k == ord('d'): # right
      u_off += 0.02
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
    cube.set_offset((u_off, v_off))
