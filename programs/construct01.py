#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

""" A reasonable scale for a city model would be 250 x 250 with each
block being 50 x 50 We will start out with "normal" houses being about
10 x 5 and offices 10 x 10

To begin with the new City class will be here in the "main" file, as it
gets bigger it will be tidied into its own file.

If you look
"""
class City(pi3d.Shape):
  def __init__(self,  camera=None, light=None, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0, tw=1.0, th=1.0, td=1.0):
    super(City, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                1.0, 1.0, 1.0, cx, cy, cz)
    buf = []


  def make_houses(self, specs):
    vertices = []
    normals = []
    tex_coords = []
    faces = []
    vn = 0
    for c in specs:
      h = c[4] # height stored in the 5th part of each spec
      """ these single letter variables are generally short-cuts to reduce
      retyping lots of characters. 
      """
      c = [(i[0], 0.0, i[1]) for i in c[:4]] # add y values 0.0 for bottoms 
      e = ((c[0][0], 0.7 * h, c[0][2]), # vertices for the eaves 70% of full height
           (c[1][0], 0.7 * h, c[1][2]),
           (c[2][0], 0.7 * h, c[2][2]),
           (c[3][0], 0.7 * h, c[3][2]))
      """ the pitch of the roof is at height h and mid way between the first
      and second, and third and fourth vertices.
      """
      p = (((c[0][0] + c[1][0]) / 2.0, h, (c[0][2] + c[1][2]) / 2.0),
           ((c[2][0] + c[3][0]) / 2.0, h, (c[2][2] + c[3][2]) / 2.0))
      """ there have to be vertices for each normal direction at a given
      corner. If we just had one vertex and one normal direction then the
      sides would blend smoothly across faces which we don't want.

      If you look at the two vertices for each end of the pitch p[0] and
      p[1] you will see they crop up three times each, that's because there
      will be planes facing in three different directions at those points.

      There are 26 vertices in total 4 x 4 sides 2 x 4 roof slopes and
      2 x top gables. The top triangles of the gables can re-use the
      vertices from the eaves that point in the same direction: the 3rd
      and 4th, and 11th and 12th below.
      """
      vertices.extend([c[0], c[1], e[1], e[0], c[1], c[2], e[2], e[1],
                  c[2], c[3], e[3], e[2], c[3], c[0], e[0], e[3],
                  p[0], p[1],
                  e[1], e[2], p[1], p[0], e[3], e[0], p[0], p[1]])
      """ these are short cuts to save typing out the names of the function
      in full several times. The following few lines may appear difficult
      but they really show the wonder of vector algebra so just hold on
      for a few seconds (then google "cross product 3D") Basically this
      is a very neat way of finding a direction that's perpendicular to
      two other directions. In this case we want a direction 90 degrees
      to the vertical edge of a wall and 90 degrees to the horizontal top
      of the wall. Or to two edges of each roof plane.

      So what each line does is do a vector subtraction of two points to
      give a vector along an edge. Then take the cross product of those
      two vectors. Then normalize, or scale, that vector so it has length
      equal to 1.0.
      """
      s_fn = pi3d.Utility.vec_sub # vector subtraction
      c_fn = pi3d.Utility.vec_cross # 3D vector cross product
      n_fn = pi3d.Utility.vec_normal # vector normalization
      n = (n_fn(c_fn(s_fn(c[1],e[1]), s_fn(c[1],c[0]))),
           n_fn(c_fn(s_fn(c[2],e[2]), s_fn(c[2],c[1]))),
           n_fn(c_fn(s_fn(c[3],e[3]), s_fn(c[3],c[2]))),
           n_fn(c_fn(s_fn(c[0],e[0]), s_fn(c[0],c[3]))),
           n_fn(c_fn(s_fn(e[2],p[1]), s_fn(e[2],e[1]))),
           n_fn(c_fn(s_fn(e[1],p[0]), s_fn(e[0],e[3]))))
      """ finally extend the list of normals to match the vertices above
      """
      normals.extend([n[0], n[0], n[0], n[0], n[1], n[1], n[1], n[1],
                 n[2], n[2], n[2], n[2], n[3], n[3], n[3], n[3],
                 n[0], n[2],
                 n[4], n[4], n[4], n[4], n[5], n[5], n[5], n[5]])
      """ If you look at the house.jpg file used to texture the houses
      you will find that it has been divided vertically into three and
      horizontally in two. t is a list of the twelve corners of each of the
      nine areas created. There are also two point a quarter and three
      quarters along the top to allow the triangular tops of the gable
      walls to be uv mapped with only a little distortion. NB (0.0, 0.0)
      is top left.
      """
      t = ((0.0, 1.0), (0.5, 1.0), (1.0, 1.0),
           (0.0, 2.0/3), (0.5, 2.0/3), (1.0, 2.0/3),
           (0.0, 1.0/3), (0.5, 1.0/3), (1.0, 1.0/3),
           (0.0, 0.0), (0.5, 0.0), (1.0, 0.0),
           (0.25, 0.0),(0.75, 0.0))
      """ the quads are arranged gable, side, gable, side, gable pitches
      and finally the two flats of the roof
      """
      tex_coords.extend([t[4], t[3], t[6], t[7], t[2], t[1], t[4], t[5],
                    t[5], t[4], t[7], t[8], t[1], t[0], t[3], t[4],
                    t[12], t[13],
                    t[7], t[6], t[9], t[10], t[8], t[7], t[10], t[11]])
      """ finally the triangles are defined. There are 14 triangles for
      each house. Each number in each of the tuples refers to an index
      in the vertex array so the increment for each house is the number
      of vertices per house.
      """
      faces.extend([(vn + i[0], vn + i[1], vn + i[2]) for i in [(0, 1, 2),
                    (0, 2, 3), (4, 5, 6), (4, 6, 7), (8, 9, 10), (8, 10, 11),
                    (12, 13, 14), (12, 14, 15), (3, 2, 16), (11, 10, 17),
                    (18, 19, 20), (18, 20, 21), (22, 23, 24), (22, 24, 25)]])
      vn += 26 # number of vertices for each house

    self.houses = pi3d.Buffer(self, vertices, tex_coords, faces, normals)
    self.buf.append(self.houses)


display = pi3d.Display.create(w=800, h=600)
CAMERA = pi3d.Camera()
shader = pi3d.Shader("uv_light")
city = City(camera=CAMERA, z=40.0)
""" the __init__ method hasn't made any Buffer object so this won't draw()
we need to run the make_houses method to generate some houses.

Add some more. Try making them really wonky.
"""
specs = (((0,0), (1,5), (8,6), (9,-1), 6.5),
         ((-1,-8), (-3,-2), (6,-3), (7,-9), 5.5),
         ((9.5,0), (10,5), (18,6), (19,-1), 9.5))
city.make_houses(specs)
""" NB all the houses are combined into one Buffer. pi3d needs a different
Buffer for each Texture so we will make a houses, offices, sidewalks, roads
etc.
"""
tex = pi3d.Texture("house.jpg")
city.set_shader(shader)
""" we left a short cut to the Buffer we created for houses called "houses"
so we have to use that to specify the Texture to use
"""
city.houses.set_textures([tex])
keys = pi3d.Keyboard()
rot, tilt = 0.0, 0.0
xm, ym, zm = 0.0, 1.5, 0.0
while display.loop_running():
  CAMERA.reset()
  CAMERA.rotate(tilt, rot, 0)
  CAMERA.position((xm, ym, zm))
  city.draw()
  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # forward
      xm += CAMERA.mtrx[0, 3]
      zm += CAMERA.mtrx[2, 3]
    elif k == ord('s'): # backwards
      xm -= CAMERA.mtrx[0, 3]
      zm -= CAMERA.mtrx[2, 3]
    elif k == ord('a'): # clockwise y axis
      rot += 2.5
    elif k == ord('d'): # anti-clockwise y axis
      rot -= 2.5
    elif k == ord('r'): # tilt up
      tilt += 2.5
    elif k == ord('f'): # tilt down
      tilt -= 2.5

keys.close()
display.destroy()
