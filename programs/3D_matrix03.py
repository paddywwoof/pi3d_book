#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
import math

display = pi3d.Display.create(w=800, h=600)

CAMERA = pi3d.Camera(is_3d=True)
matsh = pi3d.Shader("mat_flat")
lightsh = pi3d.Shader("mat_light")

""" Here we just use the ready made pi3d Cuboid shape. Also, the matrices
are not printed out as they would be identical to 3D_matrix02
"""
cube = pi3d.Cuboid(camera=CAMERA, w=200, h=200, d=200, z=500.0)
cube.set_material((1.0,0.8,0.05))
cube.set_shader(lightsh)

keys = pi3d.Keyboard()

xaxis = pi3d.Lines(camera=CAMERA, vertices=[[-250,0,0],[250,0,0]], z=1.0,
                    material=(0.0,1.0,1.0), line_width=2)
xaxis.set_shader(matsh)
yaxis = pi3d.Lines(camera=CAMERA, vertices=[[0,250,0],[0,-250,0]], z=1.0,
                    material=(0.0,1.0,1.0), line_width=2)
yaxis.set_shader(matsh)
########################################################################
## still slightly complicated but simpler than home-made text
l_font = pi3d.Font("fonts/FreeSans.ttf")
letters = pi3d.MergeShape(z=500)
for l in [["0", -120, -120, 100],
          ["1", -120, 120, 100],
          ["2", 120, -120, 100],
          ["3", 120, 120, 100]]:
  string = pi3d.String(font=l_font, string=l[0])
  letters.merge(string, x=l[1], y=l[2], z=l[3], sx=200, sy=200)
l_shader = pi3d.Shader("uv_flat")
letters.set_draw_details(l_shader, [l_font])
########################################################################
while display.loop_running():
  cube.draw()
  letters.draw()
  xaxis.draw()
  yaxis.draw()

  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # up
      cube.translateY(5.0)
      letters.translateY(5.0)
    elif k == ord('s'): # down
      cube.translateY(-5.0)
      letters.translateY(-5.0)
    elif k == ord('a'): # left
      cube.translateX(-5.0)
      letters.translateX(-5.0)
    elif k == ord('d'): # right
      cube.translateX(5.0)
      letters.translateX(5.0)
    elif k == ord('z'): # clockwise z
      cube.rotateIncZ(-2.5)
      letters.rotateIncZ(-2.5)
    elif k == ord('x'): # anti-clockwise z
      cube.rotateIncZ(2.5)
      letters.rotateIncZ(2.5)
    elif k == ord('c'): # clockwise x
      cube.rotateIncX(-2.5)
      letters.rotateIncX(-2.5)
    elif k == ord('v'): # anti-clockwise x
      cube.rotateIncX(2.5)
      letters.rotateIncX(2.5)
    elif k == ord('b'): # clockwise y
      cube.rotateIncY(-2.5)
      letters.rotateIncY(-2.5)
    elif k == ord('n'): # anti-clockwise y
      cube.rotateIncY(2.5)
      letters.rotateIncY(2.5)

keys.close()
display.destroy()
