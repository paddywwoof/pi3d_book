#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
import math

display = pi3d.Display.create(w=800, h=600, samples=4)

CAMERA = pi3d.Camera(is_3d=False)
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
cube = pi3d.Lines(camera=CAMERA, vertices=vertices, closed=True,
                    material=(1.0,0.8,0.05), line_width=3)
cube.set_shader(matsh)
t_mat = [[1.0, 0.0, 0.0, 0.0], # translation matrix
         [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 400.0], # though vertices centred on origin move away to be able to view (try changing this)
         [0.0, 0.0, 0.0, 1.0]]
rz_mat = [[1.0, 0.0, 0.0, 0.0], # z rotation matrix
         [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
rx_mat = [[1.0, 0.0, 0.0, 0.0], # x rotation matrix
         [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
ry_mat = [[1.0, 0.0, 0.0, 0.0], # y rotation matrix
         [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
dist = 500.0 # z distance of projection plane from origin, try changing it
p_mat = [[1.0, 0.0, 0.0, 0.0], # projection matrix
         [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 1.0 / dist, 0.0]]
         
angle = [0.0, 0.0, 0.0] # keep track of the angles so they can be incremented for rotation

def mat_mult(mat, vec): # if vec is matrix of the right shape multiply together
  return [m[0] * vec[0] + m[1] * vec[1] + m[2] * vec[2] + m[3] * vec[3] for m in mat]

def refresh_vertices(shape, old_verts):
  new_verts = []  # start off with a new list of vectors to keep the original ones 'clean'
  for i, v in enumerate(old_verts):
    new_v = [v[0], v[1], v[2], 1.0] # i.e. x, y, z, 1.0 to match 4x4 matrix
    new_v = mat_mult(rz_mat, new_v) # multiply by z rotation matrix
    new_v = mat_mult(rx_mat, new_v) # then multiply by x rotation matrix
    new_v = mat_mult(ry_mat, new_v) # then multiply by y rotation matrix
    """ NB see what happens if you change the order of the above lines then
    repeat the same rotation  (i.e. press z 20 times then c 20 times then
    b 20 times and take a note of the final position)
    """
    new_v = mat_mult(t_mat, new_v) # then by translation
    new_v = mat_mult(p_mat, new_v) # then by projection
    new_v = [new_v[j] / new_v[3] for j in [0,1,2]]
    new_verts.append(new_v) # finally add this to the new list of vectors
  shape.re_init(pts=new_verts) # finally update the vertex locations

def print_matrices():
  head_str = "              translation                 x rotation                    y rotation                 z rotation"
  if hasattr(keys,"key"):
    keys.key.addstr(1, 0, head_str)
  else:
    print(head_str)
  for i in range(4):
    t, rx, ry, rz = t_mat[i], rx_mat[i], ry_mat[i], rz_mat[i]
    out_str = ("{:6.1f},{:6.1f},{:6.1f},{:6.1f} |{:6.3f},{:6.3f},{:6.3f},{:6.3f} |{:6.3f},{:6.3f},{:6.3f},{:6.3f} |{:6.3f},{:6.3f},{:6.3f},{:6.3f}"
            .format(t[0], t[1], t[2], t[3], rx[0], rx[1], rx[2], rx[3], ry[0], ry[1], ry[2], ry[3], rz[0], rz[1], rz[2], rz[3]))
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
l_verts = [[-100,-100,100],[-100 - w[0],-100,100],[-100 - w[0],-140,100],[-100,-140,100],
           [-100, 140,100],[-100 - w[1], 140,100],[-100 - w[1], 100,100],[-100, 100,100],
           [100 + w[2], 140,100],[100, 140,100],[100, 100,100],[100 + w[2], 100,100],
           [100 + w[3],-100,100],[100,-100,100],[100,-140,100],[100 + w[3],-140,100]]
l_faces = [[2,1,0],[0,3,2], [6,5,4],[4,7,6], [10,9,8],[8,11,10], [14,13,12],[12,15,14]]
letters = pi3d.Shape(CAMERA, None, None, 0.0, 0.0, 0.0,  0.0, 0.0, 0.0,
                                       1.0, 1.0, 1.0,   0.0, 0.0, 0.0)
letters.buf = [pi3d.Buffer(letters, pts=l_verts, texcoords=l_texcoord, faces=l_faces)]
l_shader = pi3d.Shader("uv_flat")
letters.set_draw_details(l_shader, [l_font])
########################################################################

refresh_vertices(cube, vertices) # the matrix multiplication initially
refresh_vertices(letters, l_verts) # after this just do it if a button is pressed
while display.loop_running():
  cube.draw()
  letters.draw()
  xaxis.draw()
  yaxis.draw()

  k = keys.read()
  if k > -1:
    rotation = -1
    if k == 27:
      break
    elif k == ord('w'): # up
      t_mat[1][3] += 5.0 # NB the translation values are in the 'extra' column added on the right
    elif k == ord('s'): # down
      t_mat[1][3] -= 5.0
    elif k == ord('a'): # left
      t_mat[0][3] -= 5.0
    elif k == ord('d'): # right
      t_mat[0][3] += 5.0
    elif k == ord('z'): # clockwise z
      angle[2] += 0.05 # radians!
      rotation = 2
    elif k == ord('x'): # anti-clockwise z
      angle[2] -= 0.05 # radians!
      rotation = 2
    elif k == ord('c'): # clockwise x
      angle[0] += 0.05 # radians!
      rotation = 0
    elif k == ord('v'): # anti-clockwise x
      angle[0] -= 0.05 # radians!
      rotation = 0
    elif k == ord('b'): # clockwise y
      angle[1] += 0.05 # radians!
      rotation = 1
    elif k == ord('n'): # anti-clockwise y
      angle[1] -= 0.05 # radians!
      rotation = 1

    if rotation > -1: # 0 for rotation about x, 1 for y, 2 for z.
      c = math.cos(angle[rotation]) # do the trig functions once here
      s = math.sin(angle[rotation]) # 
      if rotation == 0:
        mat = rx_mat
      elif rotation == 1:
        mat = ry_mat
      else:
        mat = rz_mat
      a = (1 + rotation) % 3 # i.e. rotation=0->a=1, 1->a=2, 2->a=0
      b = (2 + rotation) % 3 #               0->b=2, 1->b=0, 2->b=1
      """Watch what happens to the matrices as you press the buttons to
      rotate the cube. You will see that they behave exactly as the 2D
      matrix but with an extra row and column pushed in. So in 2D we were
      effectively rotating about the z axis:
       c  s
      -s  c
        z rot     y rot     x rot   in 3D
       c  s  0   c  0 -s   1  c  s
      -s  c  0   0  1  0   0  1  0
       0  0  1   s  0  c   0 -s  c
      """
      mat[a][a] = mat[b][b] = c
      mat[a][b] = s
      mat[b][a] = -s
    print_matrices()
    refresh_vertices(cube, vertices)
    refresh_vertices(letters, l_verts)


