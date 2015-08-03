import demo
import pi3d
import time

text = """This is an example of using the pi3d.String class.
The next example will use FixedString for comparison.

Note that the shader has to use texture coordinates to work
i.e. a uv_ type. Try using uv_light, swapping justify R or
L and scaling with the sx, sy version. See the effect of
setting mipmap=False in the Font.

See if you can reduce the frame rate by reducing N or
by running string1.draw() many times each frame
"""
fps = "000.00FPS"
N = 100
FONT_SCALE = 0.005

DISPLAY = pi3d.Display.create()
CAMERA = pi3d.Camera()
CAMERA2D = pi3d.Camera(is_3d=False)

font = pi3d.Font("fonts/FreeSans.ttf", color="#FF8010") # mipmap=False)
#font.blend = True
string1 = pi3d.String(camera=CAMERA, font=font, string=text, z=4.0, justify="C")
#string1 = pi3d.String(camera=CAMERA, font=font, string=text, sx=FONT_SCALE,
#            sy=FONT_SCALE, z=5.0)
string2 = pi3d.String(camera=CAMERA2D, is_3d=False, font=font, string=fps,
            x=-DISPLAY.width / 2 + 200, y=DISPLAY.height / 2 - 75, z=1.0)

shader = pi3d.Shader('uv_flat')
#shader = pi3d.Shader('uv_light')
#shader = pi3d.Shader('mat_light')

string1.set_shader(shader)
string2.set_shader(shader)

mykeys = pi3d.Keyboard()

last_tm = time.time()
i = 0
while DISPLAY.loop_running():
  string1.rotateIncY(0.5)
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
