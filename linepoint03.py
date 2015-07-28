import sys
sys.path.insert(1,'/home/jill/pi3d')
import pi3d
    
DISPLAY = pi3d.Display.create(samples=0)
CAMERA = pi3d.Camera()

unit = pi3d.Helix(loops=2, rise=4.0)

shader = pi3d.Shader('mat_flat')
lshader = pi3d.Shader('mat_light')
from random import random
shape = pi3d.MergeShape(z=10.0)
bfr_list = []
""" There are two methods of passing objects to merge() one is as above,
one object at a time. An alternative, faster, method builds up a list
first then merges this in one step. On a slower machine, such as the
Raspberry Pi A or B you might see the difference if you comment out the
line above and use the two lines below instead.
"""
#"""
for i in range(30):
  x, y, z = random() * 8.0 - 4.0, random() * 8.0 - 4.0, random() * 8.0 - 4.0
  rot, sc = random() * 90, random() + 0.5
  shape.merge(unit, x=x, y=y, z=z, rx=rot, rz=rot, sx=sc, sy=sc, sz=sc) #"""
  #bfr_list.append([unit, x, y, z, rot, 0.0, rot, sc, sc, sc])
#shape.merge(bfr_list)

""" Comment out the for block above and produce a radialCopy instead with
the line below
"""
#shape.radialCopy(unit, startRadius=4.0, endRadius=4.0, step=30.0)

mykeys = pi3d.Keyboard()
dd = 0.01

while DISPLAY.loop_running():
  shape.set_material((0.5, 0.2, 0.7))
  shape.set_line_width(0)
  shape.draw(shader=lshader)
  shape.translateX(-CAMERA.mtrx[0, 3] * dd)
  shape.translateY(-CAMERA.mtrx[1, 3] * dd)
  shape.translateZ(-CAMERA.mtrx[2, 3] * dd)
  shape.set_material((1.0, 0.8, 0.0))
  shape.set_line_width(2, strip=False)
  shape.draw(shader=shader)
  shape.translateX(CAMERA.mtrx[0, 3] * dd)
  shape.translateY(CAMERA.mtrx[1, 3] * dd)
  shape.translateZ(CAMERA.mtrx[2, 3] * dd)
  shape.rotateIncY(0.21)
  shape.rotateIncX(0.1)

  key = mykeys.read()
  if key==27:
    mykeys.close()
    DISPLAY.destroy()
    break
