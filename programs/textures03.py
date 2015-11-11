#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
import numpy as np

display = pi3d.Display.create(x=50, y=50, w=800, h=600)

CAMERA = pi3d.Camera(is_3d=True)
shader = pi3d.Shader("uv_reflect")

cube = pi3d.Cuboid(camera=CAMERA, w=2.0, h=2.0, d=2.0, z=5.0)
""" Taking the code of texture02.py this example shows how a numpy array
can be used as a texture. The array has to be a compatible form i.e. HxWx4
or HxWx3 of unint8 bytes.
pi3d can also use PIL Image object to create a Texture. However in order to be
used in update_ndarray() they would have to be converted to numpy arrays
Image.fromarray().
"""
im = np.random.randint(0, 2, 128 * 128 * 3).astype("uint8") * 255
im.shape = (128, 128, 3)
tex = pi3d.Texture(im)
bump = pi3d.Texture("rocktile2.jpg")
refl = pi3d.Texture("glassbuilding.jpg")
cube.set_draw_details(shader, [tex, bump, refl], 2.0, 0.3, 2.0, 2.0)
u_off, v_off = 0.0, 0.0
keys = pi3d.Keyboard()
f = 0
while display.loop_running():
  cube.draw()
  if f % 3 == 0: # only do this every three frames
    i = int(f / 3) % 3 # cycle between RGB values
    #im[:,:,:i] += np.random.randint(0,4,(128, 128, 1))
    #"""
    # alternatively the following does a Conways game of life on the pixels.
    # comment out the above randint() line and the triple quotes around
    # this docstring
    im[:,:,i] /= 16 # uint8 overflows if you try to add values up
    N = (im[0:-2,0:-2,i] + im[0:-2,1:-1,i] + im[0:-2,2:,i] +
         im[1:-1,0:-2,i]                   + im[1:-1,2:,i] +
         im[2:  ,0:-2,i] + im[2:  ,1:-1,i] + im[2:  ,2:,i])
    birth = (N==45) & (im[1:-1,1:-1,i]==0) # 3 cells @ int(255 / 16) => 15
    survive = ((N==30) | (N==45)) & (im[1:-1,1:-1,i]==15)
    im[:,:,i] = 0
    im[1:-1,1:-1,i][birth | survive] = 255
    #"""

    tex.update_ndarray(im)
    """ NB the Tecture has to have the OpenGL buffer updated in order for
    the modified array to take effect
    """
  f += 1
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

keys.close()
display.destroy()
