#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

DISPLAY = pi3d.Display.create(x=150, y=150)
shader = pi3d.Shader("uv_flat")
CAMERA = pi3d.Camera(is_3d=False)
tex1 = pi3d.Texture("techy1.jpg")
#tex1 = pi3d.Texture("techy2.png")
tex2 = pi3d.Texture("glassbuilding.jpg")
#tex2 = pi3d.Texture("techy2.png")
z1 = 5.0 # z value of sprite1
a1 = 1.0 # alpha value of sprite1
a2 = 1.0 # alpha value of sprite2
sprite1 = pi3d.Sprite(w=400.0, h=400.0, x=-100.0, y=100.0, z=z1)
sprite1.set_draw_details(shader, [tex1])

sprite2 = pi3d.Sprite(w=400.0, h=400.0, x=100.0, y=-100.0, z=z1 + 0.2)
sprite2.set_draw_details(shader, [tex2])
""" The two Sprites start off overlapping with sprite2 slightly further
away. Both have default alpha value of 1.0
"""
keys = pi3d.Keyboard()
while DISPLAY.loop_running():
  sprite1.draw()
  sprite2.draw()
  """ Keys w,s move sprite1 back,forward a,d decrease,increase sprite1
  alpha and z,c decrease,increase sprite2 alpha

  NB sprite2 is drawn after sprite1 see what happens if sprite1 is in
  front of sprite2 as you reduce the alpha so you can see through it. Now
  put sprite2 in front and reduce its alpha.

  Try swapping tex1 and tex2 (one at a time) to techy2.png, move them back
  and forth and change their alpha values.
  """
  
  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # away
      z1 += 0.1
    elif k == ord('s'): # nearer
      z1 -= 0.1
    elif k == ord('a'): # less solid sprite1
      a1 -= 0.05
    elif k == ord('d'): # more solid sprite1
      a1 += 0.05
    elif k == ord('z'): # less solid sprite2
      a2 -= 0.05
    elif k == ord('c'): # more solid sprite2
      a2 += 0.05
    sprite1.positionZ(z1)
    sprite1.set_alpha(a1)
    sprite2.set_alpha(a2)
