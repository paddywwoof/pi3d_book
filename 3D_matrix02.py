#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
import math

display = pi3d.Display.create(w=800, h=600)

""" We are now using pi3d and OpenGL to do the matrix multiplication so we set
the camera to do the 3D projection for us.
"""
CAMERA = pi3d.Camera(is_3d=True)
matsh = pi3d.Shader("mat_flat")
############## x  #### y  ### z
vertices = [[-100.0, -100.0, -100.0],
            [-100.0,  100.0, -100.0],
            [ 100.0,  100.0, -100.0],
            [ 100.0, -100.0, -100.0],
            [ 100.0, -100.0, 100.0],
            [ 100.0,  100.0, 100.0],
            [-100.0,  100.0, 100.0],
            [-100.0, -100.0, 100.0]]
""" The Lines object draws a line connecting vertices, if we pass the
closed argument it will connect back to the start vertex.
"""
cube = pi3d.Lines(camera=CAMERA, vertices=vertices, closed=True, z=500.0,
                    material=(1.0,0.8,0.05), line_width=3)
cube.set_shader(matsh)

""" Notice how the matrices have been transposed and look different from
before. If we used these in our previous mat_mult() function they would
give the wrong answer. However the Fortran convention is the default used
by OpenGL where M[i][j] refers to the column i and the row j whereas the
python (and C) convention is that M[i][j] refers to row i and column j.

The Fortran and OpenGL style is the conventional way of indexing matrices
used in mathematic notation and will probably match examples you see on
Wikipedia etc. In order to pass the model transformation and projection
matrices to the shader, pi3d holds them in Fortran orientation.
"""
def print_matrices():
  head_str = "              translation                 x rotation                    y rotation                 z rotation"
  if hasattr(keys,"key"):
    keys.key.addstr(1, 0, head_str)
  else:
    print(head_str)
  for i in range(4):
    t, rx, ry, rz = cube.tr1[i], cube.rox[i], cube.roy[i], cube.roz[i]
    out_str = ("{:6.1f},{:6.1f},{:6.1f},{:6.1f} |{:6.3f},{:6.3f},{:6.3f},{:6.3f} |{:6.3f},{:6.3f},{:6.3f},{:6.3f} |{:6.3f},{:6.3f},{:6.3f},{:6.3f}"
            .format(t[0], t[1], t[2], t[3], rx[0], rx[1], rx[2], rx[3], ry[0], ry[1], ry[2], ry[3], rz[0], rz[1], rz[2], rz[3]))
    if hasattr(keys,"key"): # curses set up
      keys.key.addstr(2 + i, 0, out_str)
    else:
      print(out_str)

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
      """ The matrix multiplication is done using numpy.dot() function as part
      of the Shape.draw() method. This seems to be the fastest way to do it!

      Shape has various utility methods for updating the translation, rotation
      scale matrices held for each object.
      """
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
    print_matrices()
