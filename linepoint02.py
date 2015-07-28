import demo
import pi3d
    
DISPLAY = pi3d.Display.create(samples=4)
CAMERA = pi3d.Camera()

shape = pi3d.Helix(ringrots=16, sides=36, loops=4, rise=4.0, z=5.0) 
#shape = pi3d.Model(file_string='model01.obj', z=8.0) # straight from blender
#shape = pi3d.Model(file_string='model02.obj', z=8.0) # revised order of faces
shader = pi3d.Shader('mat_flat')
lshader = pi3d.Shader('mat_light')

mykeys = pi3d.Keyboard()

""" Try changing dd to bigger values, or 0 or -ve. Also see what happens
with different values of line width - is there a maximum or minimum value?

With a pi3d.Model object you will see that the default order of faces produced
by blender produces a cat's cradle of lines. Correcting this is non-trivial.
"""
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
