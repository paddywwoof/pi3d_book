#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
import time

text = """This is an example of using the pi3d.FixedString class.
Compare behaviour with the previous example.

Note that the shader has to use texture coordinates to work
i.e. a uv_ type. Try different shaders and different filter
types (f_type argument)

See if you can reduce the frame rate by reducing N or
by running string1.draw() many times each frame
"""
fps = "000.00FPS"
N = 100

DISPLAY = pi3d.Display.create(x=50, y=50)
CAMERA = pi3d.Camera()
CAMERA2D = pi3d.Camera(is_3d=False)
font = pi3d.Font("fonts/FreeSans.ttf", color="#FF8010")

string1 = pi3d.FixedString(camera=CAMERA, font="fonts/FreeSans.ttf", string=text,
            color="#FF8010", justify="C") # mipmap=False
#string1 = pi3d.FixedString(camera=CAMERA, font="fonts/FreeSans.ttf", string=text,
#            color="#FF8010", justify="L", f_type="", # try BUMP , EMBOSS, CONTOUR, BLUR, SMOOTH
#            background_color=(255,200,255,100))
string1.sprite.scale(0.03, 0.03, 1.0)
""" the built-in Sprite works nicely with 2D camera where 1 unit is 1 pixel
but needs drastic scaling down (as above) to work with the perspective camera"""
string2 = pi3d.String(camera=CAMERA2D, is_3d=False, font=font, string=fps,
            x=-DISPLAY.width / 2 + 200, y=DISPLAY.height / 2 - 75, z=1.0)

shader = pi3d.Shader('uv_flat')
lshader = pi3d.Shader('uv_light')

string1.set_shader(lshader)
string2.set_shader(shader)
mykeys = pi3d.Keyboard()

last_tm = time.time()
i = 0
while DISPLAY.loop_running():
  string1.sprite.rotateIncY(0.5)
  #for k in range(50): #NB you will need to indent following line
  string1.draw()
  i += 1
  if i > N:
    tm = time.time()
    fps = "{:6.2f}FPS".format(i / (tm - last_tm))
    string2.quick_change(fps)
    i = 0
    last_tm = tm
  string2.draw()
  
  key = mykeys.read()
  if key==27:
    mykeys.close()
    DISPLAY.destroy()
    break

mykeys.close()
DISPLAY.destroy()
