#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
import math

display = pi3d.Display.create(w=800, h=600, samples=4)

CAMERA = pi3d.Camera(is_3d=True)
shader = pi3d.Shader("uv_light")
#shader = pi3d.Shader("uv_flat")
l_vec = [0.7, -0.7, 2.5]
light = pi3d.Light(l_vec,
                   (0.5, 1.0, 0.7),
                   (0.3, 0.1, 0.1), is_point=False)
cube = pi3d.Cuboid(camera=CAMERA, w=1.5, h=1.5, d=1.5, z=4.0)
#cube = pi3d.Cuboid(camera=CAMERA, w=15.0, h=15.0, d=15.0, z=40.0) # more distant cube
tex = pi3d.Texture("techy1.jpg")
cube.set_draw_details(shader, [tex])
""" Modifying the code of texture01.py, this example explicitly creates a
Light object rather than using the default instance. For directional lighting
it doesn't matter where the object to be illuminated is, but for a point
light it does. Because of this the cube is scaled down and positioned just
a little bit further away than the z position of l_vec.

The z,x,c,v,b,n keys still rotate the cube but w,a,s,d change the x and
y components of l_vec. Try moving the light and rotating the cube then
alter the code to make is_point=True and do the same again.

With the directional light try changing the RGB values of the Light and
the ambient light. Try increasing them to large values such as 5.0 or 20.0.
Now try it with is_point=True, try switching the cube to the more distant
version commented out above. In order for the point light to illuminate it
you will have to increase the RBG values significantly (and move the light
source a long way either side to get shadows forming)   
"""
#####
light_obj = pi3d.Lines(vertices=((0.0,0.0,0.0), l_vec ,
                                [0.95 * l_vec[0], l_vec[1], l_vec[2]],
                                [l_vec[0], 0.95 * l_vec[1], l_vec[2]],
                                l_vec), line_width=4.0)
flatsh = pi3d.Shader("mat_flat")
light_obj.set_shader(flatsh)
""" This section is for drawing an arrow to indicate l_vec. Don't get
diverted by the issues of drawing lines at this stage but note that the line
starts at the origin (position of Camera) but only the part that is further
away than the near plane (DEFAULT_NEAR = 1.0 in Display) is visible. The
location and effect of the far plane will be shown in the next example
texture02.py
"""
#####
keys = pi3d.Keyboard()
while display.loop_running():
  cube.draw()
  light_obj.draw()

  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # up
      l_vec[1] += 0.1
    elif k == ord('s'): # down
      l_vec[1] -= 0.1
    elif k == ord('a'): # left
      l_vec[0] -= 0.1
    elif k == ord('d'): # right
      l_vec[0] += 0.1
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
    light.position(l_vec)
    cube.set_light(light)
    light_obj = pi3d.Lines(vertices=((0.0,0.0,0.0), l_vec ,
                                  [0.95 * l_vec[0], l_vec[1], l_vec[2]],
                                  [l_vec[0], 0.95 * l_vec[1], l_vec[2]],
                                  l_vec), line_width=4.0)
    light_obj.set_shader(flatsh)

