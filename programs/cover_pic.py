#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
from math import *
import numpy as np #####################################################

class Twist(pi3d.Shape):
  """ generates a parametric surface
  """
  def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0,
    x=0.0, y=0.0, z=0.0,
    rx=0.0, ry=0.0, rz=0.0,
    sx=1.0, sy=1.0, sz=1.0,
    cx=0.0, cy=0.0, cz=0.0):
    
    super(Twist, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
      sx, sy, sz, cx, cy, cz)
    
    self.ttype = pi3d.GL_TRIANGLES

    res_u = 256
    res_v = 32
    ####################################################################
    image = [[[0, 0, 0] for i in range(res_u)] for j in range(res_v)]
    
    def rotarywhirly(u, v, r=0.25, para1=1, para2=5, para3=2,
                                   para4=1, para5=5, para6=2,
                                   para7=0.2, para8=2):
      U = 2 * pi * u
      V = 2 * pi * v
      x = cos(para2 * U) * (para1 + r * sin(V) + para3 * r * cos(U))
      y = sin(para5 * U) * (para4 + r * sin(V) + para6 * r * cos(U))
      z = para7 * r * cos(V) + para8 * r * sin(U)
      r = 0.5 + 0.5 * sin(U)
      g = 0.5 + 0.5 * sin(para3 * U - V)
      b = 0.5 + 0.5 * sin(para2 * U + V)
      return x, y, z, r, g, b ##########################################
            
    verts = []
    uv = []
    for j in range(res_v):
      v =  j / (res_v - 1.0)
      for i in range(res_u):
        u =  i / (res_u - 1.0)
        x, y, z, r, g, b = rotarywhirly(u, v, 0.6, 1, 5, 2, 1, 4, 3, 0.4, 3)
        verts.append((x, y, z))
        uv.append((u, v)) ##############################################
        image[j][i] = [int(r * 255), int(g * 255), int(b * 255)]

    self.im = np.array(image, dtype="uint8") ###########################

    inds0 = []
    inds1 = []
    self.buf = []
    for i in range(res_v-1):
      for j in range(res_u-1):
        a = i * res_u + j
        b = a + res_u
        c = b + 1
        d = a + 1
        inds0.append((b, a, d))
        inds0.append((c, b, d))
        inds1.append((a, b, d))
        inds1.append((b, c, d))

    buff = pi3d.Buffer(self, verts, uv, inds0)
    buff.set_material((1.0, 0.0, 0.0))
    self.buf.append(buff)
    buff = pi3d.Buffer(self, verts, uv, inds1)
    buff.set_material((0.0, 1.0, 1.0))
    self.buf.append(buff)


DISPLAY = pi3d.Display.create(samples=4)
CAMERA = pi3d.Camera()
CAMERA_2D = pi3d.Camera(is_3d=False)

curve = Twist(z=10.0)

tex1 = pi3d.Texture(curve.im, mipmap=False)
tex2 = pi3d.Texture(np.zeros((4, 4, 3)).astype("uint8")) ### no bumps
# random grey-scale reflections (by repeating values 3 times)
tex3 = pi3d.Texture(np.repeat(
              np.random.randint(0, 255, (16, 16)).
                astype("uint8"), 3).
                  reshape(16, 16, 3), mipmap=False)

shader = pi3d.Shader('uv_reflect')
curve.set_draw_details(shader, [tex1, tex2, tex3], 0.0, 0.1)

flatsh = pi3d.Shader("uv_flat")
sprite = pi3d.Sprite(w=30.0, h=30.0, z=15.0, rz=90)
sprite.set_draw_details(flatsh, [tex1], vmult=4.0)

string1 = pi3d.FixedString(camera=CAMERA, font="fonts/FreeSans.ttf",
            string=" 3D Graphics with pi3d ", color=(0,0,0), font_size=48)
w, h = string1.ix * 48.0, string1.iy * 64.0
tube = pi3d.Tube(sides=64, height=h*3.1416/w, y=1.2, z=5.0, rx=-30, rz=10)
tube.set_draw_details(shader, [string1, tex2, tex3], 0.0, 0.1, umult=4.0, vmult=4.0)
tube.set_offset((0.5, 2.0))

# Fetch key presses
mykeys = pi3d.Keyboard()
ani = False
while DISPLAY.loop_running():
  curve.draw()
  curve.rotateIncY(0.21)
  curve.rotateIncX(0.1)
  sprite.draw()
  tube.draw()
  tube.rotateIncY(0.11)
  if ani:
    # following animate colours ########################################
    curve.im += np.random.randint(0, 2, curve.im.shape)
    tex1.update_ndarray(curve.im)

  key = mykeys.read()
  if key == 27:
    mykeys.close()
    DISPLAY.destroy()
    break
  elif key == ord("z"):
    ani = not ani

mykeys.close()
display.destroy()
