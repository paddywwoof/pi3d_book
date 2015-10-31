import demo
import pi3d
import time

text = """Here the ability of FixedString to
be used as a Texture is exploided to
clothe a different shape (from the
simple plane form of String or
FixedString.sprite)

Try using different filters by changing
the f_type argument. To see the real
effect of BUMP you will need to change
the lshader to mat_bump

"""
fps = "000.00FPS"
N = 100

DISPLAY = pi3d.Display.create()
CAMERA = pi3d.Camera()
CAMERA2D = pi3d.Camera(is_3d=False)
font = pi3d.Font("fonts/FreeSans.ttf", color="#FF8010")
#font.blend = True
string1 = pi3d.FixedString(camera=CAMERA, font="fonts/FreeSans.ttf", string=text,
            color="#FF8010", justify="L", f_type="") # EMBOSS, CONTOUR, BLUR, SMOOTH, BUMP
string2 = pi3d.String(camera=CAMERA2D, is_3d=False, font=font, string=fps,
            x=-DISPLAY.width / 2 + 200, y=DISPLAY.height / 2 - 75, z=1.0)

shader = pi3d.Shader('uv_flat')
lshader = pi3d.Shader('uv_light')
#lshader = pi3d.Shader('mat_bump')

string2.set_shader(shader)

w, h = string1.ix, string1.iy
shape = pi3d.Tube(sides=64, height=(h * 3.1416)/w, z=4.0, ry=-90)
#shape.set_material((0.6, 0.5, 0.1))
shape.set_draw_details(lshader,[string1], 1.0)

mykeys = pi3d.Keyboard()

last_tm = time.time()
i = 0
while DISPLAY.loop_running():
  shape.rotateIncY(0.25)
  shape.rotateIncX(0.11)
  shape.draw()
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
