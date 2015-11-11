#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
import math

display = pi3d.Display.create(x=50, y=350, w=800, h=600)
""" Camera defined with is_3d=False does not apply any perspective when
rendering the scene and uses a convenient scale of 1 unit per pixel.
The z value of shapes can be used for layering but doesn't have a normal
3D linear interpretation. Projection matrices will be covered in a later
chapter.
"""
CAMERA = pi3d.Camera(is_3d=False)
matsh = pi3d.Shader("mat_flat")
############## x  #### y  ### z
vertices = [[-100.0, -100.0, 0.0],
            [-100.0,  100.0, 0.0],
            [ 100.0,  100.0, 0.0],
            [ 100.0, -100.0, 0.0]]
""" The Lines object draws a line connecting vertices, if we pass the
closed argument it will connect back to the start vertex.
"""
square = pi3d.Lines(camera=CAMERA, vertices=vertices, closed=True,
                    material=(1.0,0.8,0.05), line_width=3)
square.set_shader(matsh)
""" Though we are working in 2D for this demo, and 2x2 matrices should be
sufficient, to do translation requires values to be added to the x and y
components of position. By increasing the matrix to 3x3 the translation
can be done by matrix multiplication
"""
t_mat = [[1.0, 0.0, 0.0], # translation matrix
         [0.0, 1.0, 0.0],
         [0.0, 0.0, 1.0]]
r_mat = [[1.0, 0.0, 0.0], # rotation matrix
         [0.0, 1.0, 0.0],
         [0.0, 0.0, 1.0]]
s_mat = [[1.0, 0.0, 0.0], # scale matrix - all three start out as 'identity' matrices
         [0.0, 1.0, 0.0],
         [0.0, 0.0, 1.0]]
angle = 0 # keep track of the angle so it can be incremented for rotation

def mat_vec_mult(mat, vec):
  """ apply a matrix to a vector and return a modified vector
  """
  return [mat[0][0] * vec[0] + mat[0][1] * vec[1] + mat[0][2] * vec[2],
          mat[1][0] * vec[0] + mat[1][1] * vec[1] + mat[1][2] * vec[2],
          mat[2][0] * vec[0] + mat[2][1] * vec[1] + mat[2][2] * vec[2]]
    
def refresh_vertices(shape, old_verts):
  new_verts = []  # start off with a new list of vectors to keep the original ones 'clean'
  for v in old_verts:
    new_v = mat_vec_mult(s_mat, [v[0], v[1], 1.0]) # i.e. x, y, 1.0 to match 3x3 matrix
    new_v = mat_vec_mult(r_mat, new_v) # then multiply by rotation matrix
    new_v = mat_vec_mult(t_mat, new_v) # then by translation
    new_verts.append(new_v) # finally add this to the new list of vectors
    """ NB the third position in the vector will be used as the z position
    but as this is a 2D projection it has no physical meaning. Similarly
    in the 4D multiplication the final vectors may end up with a value in
    their 4th position which, though needed for the intermediate steps,
    has no physical interpretation.

    **NB** the order of the matrix multiplication makes a difference. Try
    swapping them round i.e. t-s-r, r-t-s, t-r-s and see what the effect is.
    In 3D there are 3 rotation axes and the order of rotation also matters.
    """
  shape.re_init(pts=new_verts) # finally update the vertex locations

def print_matrices():
  head_str = "        translation                 rotation                    scale"
  if hasattr(keys,"key"):
    keys.key.addstr(1, 0, head_str)
  else:
    print(head_str)
  for i in range(3):
    t, r, s = t_mat[i], r_mat[i], s_mat[i]
    out_str = ("{:8.3f},{:8.3f},{:8.3f} |{:8.3f},{:8.3f},{:8.3f} |{:8.3f},{:8.3f},{:8.3f}"
            .format(t[0], t[1], t[2], r[0], r[1], r[2], s[0], s[1], s[2]))
    if hasattr(keys,"key"): # curses set up
      keys.key.addstr(2 + i, 0, out_str)
    else:
      print(out_str)

""" pi3d uses the python curses module for keyboard input. ESC will break out
of the while loop
"""
keys = pi3d.Keyboard()

xaxis = pi3d.Lines(camera=CAMERA, vertices=[[-250,0,0],[250,0,0]], z=1.0,
                    material=(0.0,1.0,1.0), line_width=2)
xaxis.set_shader(matsh)
yaxis = pi3d.Lines(camera=CAMERA, vertices=[[0,250,0],[0,-250,0]], z=1.0,
                    material=(0.0,1.0,1.0), line_width=2)
yaxis.set_shader(matsh)
########################################################################
## This bit is rather complicated and rather non-standard, don't worry
## about it at the moment - there are much simpler ways of using text in
## pi3d 
l_font = pi3d.Font("fonts/FreeSans.ttf")
l_texcoord = []
w = []
for l in ["0","1","2","3"]:
  glyph = l_font.glyph_table[l]
  l_texcoord.extend([[i for i in j] for j in glyph[2]])
  w.append(40 * glyph[0] / glyph[1])
l_verts = [[-100,-100,0],[-100 - w[0],-100,0],[-100 - w[0],-140,0],[-100,-140,0],
           [-100, 140,0],[-100 - w[1], 140,0],[-100 - w[1], 100,0],[-100, 100,0],
           [100 + w[2], 140,0],[100, 140,0],[100, 100,0],[100 + w[2], 100,0],
           [100 + w[3],-100,0],[100,-100,0],[100,-140,0],[100 + w[3],-140,0]]
l_faces = [[2,1,0],[0,3,2], [6,5,4],[4,7,6], [10,9,8],[8,11,10], [14,13,12],[12,15,14]]
letters = pi3d.Shape(CAMERA, None, None, 0.0, 0.0, 0.0,  0.0, 0.0, 0.0,
                                       1.0, 1.0, 1.0,   0.0, 0.0, 0.0)
letters.buf = [pi3d.Buffer(letters, pts=l_verts, texcoords=l_texcoord, faces=l_faces)]
l_shader = pi3d.Shader("uv_flat")
letters.set_draw_details(l_shader, [l_font])
########################################################################

while display.loop_running():
  square.draw()
  letters.draw()
  xaxis.draw()
  yaxis.draw()

  k = keys.read()
  if k > -1:
    do_rotation = False
    if k == 27:
      break
    elif k == ord('w'): # up
      t_mat[1][2] += 5.0 # NB the translation values are in the 'extra' column added on the right
    elif k == ord('s'): # down
      t_mat[1][2] -= 5.0
    elif k == ord('a'): # left
      t_mat[0][2] -= 5.0
    elif k == ord('d'): # right
      t_mat[0][2] += 5.0
    elif k == ord('z'): # clockwise
      angle += 0.025 # radians!
      do_rotation = True
    elif k == ord('x'): # anti-clockwise
      angle -= 0.025 # radians!
      do_rotation = True
    elif k == ord('c'): # grow - scaling is simplest concept
      s_mat[0][0] = s_mat[1][1] = s_mat[0][0] * 1.025
    elif k == ord('v'): # shrink
      s_mat[0][0] = s_mat[1][1] = s_mat[0][0] * 0.975
    if do_rotation:
      """ the trigonometry isn't too tricky to work out but look at
      http://en.wikipedia.org/wiki/Rotation_matrix
      NB There are two confusing features to matrix representation in pi3d:
      One is explained in 3D_matrix02 which is the python/C convention of
      subscripts going M[row][col] whereas mathematicians are used to
      M[col][row]
      The other is the fact that the axis system in OpenGL is "right handed"
      i.e. x increases left to right, y increases upwards but z increase
      into the screen.
      """
      c = math.cos(angle)
      s = math.sin(angle)
      r_mat[0][0] = r_mat[1][1] = c
      r_mat[0][1] = s
      r_mat[1][0] = -s
    print_matrices()
    refresh_vertices(square, vertices)
    refresh_vertices(letters, l_verts)

keys.close()
display.destroy()
