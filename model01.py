#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
import numpy as np

display = pi3d.Display.create(w=800, h=600)

CAMERA = pi3d.Camera(is_3d=True)
shader = pi3d.Shader("uv_reflect")

model = pi3d.Model(camera=CAMERA, file_string="model01.obj", y=-2.0, z=10.0)
model.set_shader(shader)
bump = pi3d.Texture("rocktile2.jpg")
refl = pi3d.Texture("glassbuilding.jpg")
model.set_normal_shine(bump, 1.0, refl, 0.1)
u_off, v_off = 0.0, 0.0
keys = pi3d.Keyboard()
while display.loop_running():
  model.draw()

  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # up
      v_off += 0.01
    elif k == ord('s'): # down
      v_off -= 0.01
    elif k == ord('a'): # left
      u_off -= 0.01
    elif k == ord('d'): # right
      u_off += 0.01
    elif k == ord('z'): # clockwise z
      model.rotateIncZ(-0.5)
    elif k == ord('x'): # anti-clockwise z
      model.rotateIncZ(0.5)
    elif k == ord('c'): # clockwise x
      model.rotateIncX(-0.5)
    elif k == ord('v'): # anti-clockwise x
      model.rotateIncX(0.5)
    elif k == ord('b'): # clockwise y
      model.rotateIncY(-0.5)
    elif k == ord('n'): # anti-clockwise y
      model.rotateIncY(0.5)
    model.set_offset((u_off, v_off))
