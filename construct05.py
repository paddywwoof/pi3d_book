#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

""" City class has had make_sidewalks() added
"""
class City(pi3d.Shape):
  def __init__(self,  camera=None, light=None, name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0, tw=1.0, th=1.0, td=1.0):
    super(City, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                1.0, 1.0, 1.0, cx, cy, cz)
    buf = []


  def _make_buildings(self, specs, t_coords, eaves_h):
    vertices = []
    normals = []
    tex_coords = []
    faces = []
    vn = 0
    for c in specs:
      h = c[4] # height stored in the 5th part of each spec
      v_scale = c[5] # scale the v coordinates in t_coords in 6th part
      c = [(i[0], 0.0, i[1]) for i in c[:4]] # add y values 0.0 for bottoms 
      e = ((c[0][0], eaves_h * h, c[0][2]), # vertices for the eaves 70% of full height
           (c[1][0], eaves_h * h, c[1][2]),
           (c[2][0], eaves_h * h, c[2][2]),
           (c[3][0], eaves_h * h, c[3][2]))
      p = (((c[0][0] + c[1][0]) / 2.0, h, (c[0][2] + c[1][2]) / 2.0),
           ((c[2][0] + c[3][0]) / 2.0, h, (c[2][2] + c[3][2]) / 2.0))
      vertices.extend([c[0], c[1], e[1], e[0], c[1], c[2], e[2], e[1],
                  c[2], c[3], e[3], e[2], c[3], c[0], e[0], e[3],
                  p[0], p[1],
                  e[1], e[2], p[1], p[0], e[3], e[0], p[0], p[1]])
      s_fn = pi3d.Utility.vec_sub # vector subtraction
      c_fn = pi3d.Utility.vec_cross # 3D vector cross product
      n_fn = pi3d.Utility.vec_normal # vector normalization
      n = (n_fn(c_fn(s_fn(c[1],e[1]), s_fn(c[1],c[0]))),
           n_fn(c_fn(s_fn(c[2],e[2]), s_fn(c[2],c[1]))),
           n_fn(c_fn(s_fn(c[3],e[3]), s_fn(c[3],c[2]))),
           n_fn(c_fn(s_fn(c[0],e[0]), s_fn(c[0],c[3]))),
           n_fn(c_fn(s_fn(e[2],p[1]), s_fn(e[2],e[1]))),
           n_fn(c_fn(s_fn(e[1],p[0]), s_fn(e[0],e[3]))))
      normals.extend([n[0], n[0], n[0], n[0], n[1], n[1], n[1], n[1],
                 n[2], n[2], n[2], n[2], n[3], n[3], n[3], n[3],
                 n[0], n[2],
                 n[4], n[4], n[4], n[4], n[5], n[5], n[5], n[5]])
      tex_coords.extend([(t[0], (t[1] - 1.0) * v_scale + 1.0) for t in t_coords])
      faces.extend([(vn + i[0], vn + i[1], vn + i[2]) for i in [(0, 1, 2),
                    (0, 2, 3), (4, 5, 6), (4, 6, 7), (8, 9, 10), (8, 10, 11),
                    (12, 13, 14), (12, 14, 15), (3, 2, 16), (11, 10, 17),
                    (18, 19, 20), (18, 20, 21), (22, 23, 24), (22, 24, 25)]])
      vn += 26 # number of vertices for each house

    return pi3d.Buffer(self, vertices, tex_coords, faces, normals)


  def make_houses(self, specs):
    t = ((0.0, 1.0), (0.5, 1.0), (1.0, 1.0),
         (0.0, 2.0/3), (0.5, 2.0/3), (1.0, 2.0/3),
         (0.0, 1.0/3), (0.5, 1.0/3), (1.0, 1.0/3),
         (0.0, 0.0), (0.5, 0.0), (1.0, 0.0),
         (0.25, 0.0),(0.75, 0.0))
    t_coords = [t[4], t[3], t[6], t[7], t[2], t[1], t[4], t[5],
                t[5], t[4], t[7], t[8], t[1], t[0], t[3], t[4],
                t[12], t[13],
                t[7], t[6], t[9], t[10], t[8], t[7], t[10], t[11]]
    self.houses = self._make_buildings(specs, t_coords, 0.7)
    self.buf.append(self.houses)


  def make_offices(self, specs):
    t = ((0.0, 1.0), (1.0, 1.0),
         (0.0, 0.01), (1.0, 0.01),
         (0.0, 0.0), (1.0, 0.0),
         (0.5, 0.0))    
    t_coords = [t[1], t[0], t[2], t[3], t[1], t[0], t[2], t[3],
                    t[1], t[0], t[2], t[3], t[1], t[0], t[2], t[3],
                    t[6], t[6],
                    t[2], t[3], t[5], t[4], t[2], t[3], t[5], t[4]]
    self.offices = self._make_buildings(specs, t_coords, 0.99)
    self.buf.append(self.offices)

  def make_sidewalks(self, specs):
    vertices = []
    normals = []
    tex_coords = []
    faces = []
    vn = 0
    n = (0.0, 1.0, 0.0) # all point upwards!
    for sw in specs: # each sw in a sidewalk
      sumx = 0.0
      sumz = 0.0
      for c in sw: # each c is a corner
        c = (c[0], 0.0, c[1]) # add y = 0.0 to tuples
        e = (c[0], c[1]+0.1, c[2]) # top level
        vertices.extend([c, c, e, e])
        normals.extend([n, n, n, n])
        tex_coords.extend([(0.0, 1.0), (1.0, 1.0), (0.0, 0.9), (1.0, 0.9)])
        sumx += c[0]
        sumz += c[2]
      num = len(sw)
      vertices.extend([(sumx / num, 0.25, sumz / num)])
      normals.extend([n])
      tex_coords.extend([(0.5, 0.0)])
      numc = num * 4
      for i in range(num):
        faces.extend([(vn + i*4 + 1, vn + (i*4 + 4) % numc, vn + (i*4 + 6) % numc),
                      (vn + i*4 + 1, vn + (i*4 + 6) % numc, vn + i*4 + 3),
                      (vn + i*4 + 3, vn + (i*4 + 6) % numc, vn + numc)])
                    
      vn += numc + 1
      
    self.sidewalks = pi3d.Buffer(self, vertices, tex_coords, faces, normals)
    self.buf.append(self.sidewalks)

from construct04 import build_block_specs, shrink_block
""" blocks is a list of tuples in which the first element is a list of
corners of the block and the second element is the probability of offices

Ideally this would be produce by a clever algorithm, I will leave researching
and implementing that as an exercise!
"""
blocks = ((((65,55),(90,75),(90, 40)),0.0),
          (((65,55),(55,95),(80,105),(90,75)),0.0),
          (((55,95),(70,130),(80,105)),0.0),
          (((70,130),(102,150),(110,125),(80,105)),0.0),
          (((102,150),(125,152),(110,125)),0.1),
          
          (((125,150),(140,125),(135,120),(115,140)),0.1),
          (((115,140),(135,120),(125,110),(110,125)),0.2),
          (((135,120),(145,115),(148,100),(125,110)),0.4),
          (((125,110),(138,105),(125,75),(115,80)),0.05),
          (((138,105),(148,100),(136,65),(125,75)),0.05),
          
          (((140,80),(152,75),(145,58),(136,65)),0.2),
          (((145,58),(135,51),(128,58),(136,65)),0.05),
          (((128,58),(135,51),(125,42),(120,49)),0.05),
          (((120,49),(118,65),(125,75),(136,65)),0.3),
          (((115,80),(118,65),(90,55),(90,75)),0.3),
          
          (((118,65),(120,49),(90,40),(90,55)),0.3))

""" start of with empty spec lists then add to them by calling the
build_block_specs() function. We shrink the kerbs to 85% of the block
polygon and the buildings to 75%
"""
off_specs, hou_specs, side_specs = [], [], []
for block, o_prob in blocks:
  specs = build_block_specs(shrink_block(block, 0.75), o_prob)
  off_specs.extend(specs[0])
  hou_specs.extend(specs[1])
  side_specs.extend([shrink_block(block, 0.85)])

display = pi3d.Display.create()
CAMERA = pi3d.Camera()
LIGHT = pi3d.Light(lightamb=(0.3, 0.3, 0.5))
shader = pi3d.Shader("uv_light")
city = City(camera=CAMERA)
"""
sidewalks
"""
city.make_sidewalks(side_specs)
texs = pi3d.Texture("sidewalk.jpg")
city.sidewalks.set_textures([texs])
""" 
offices
"""
city.make_offices(off_specs)
texo = pi3d.Texture("offices.jpg")
city.offices.set_textures([texo])
"""
houses
"""
city.make_houses(hou_specs)
texh = pi3d.Texture("house.jpg")
city.houses.set_textures([texh])

city.set_shader(shader)
city.set_fog((0.4, 0.4, 0.6, 0.95), 150)

ground = pi3d.Sprite(w=200, h=200, x=100, z=100, y=0.02, rx=90)
texg = pi3d.Texture("ground.jpg")
ground.set_draw_details(shader, [texg])

keys = pi3d.Keyboard()
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()
omx, omy = mymouse.position()
rot, tilt = 0.0, -5.0
xm, ym, zm = 120.0, 20.0, 10.0
while display.loop_running():
  CAMERA.reset()
  CAMERA.rotate(tilt, rot, 0)
  CAMERA.position((xm, ym, zm))
  city.draw()
  ground.draw()

  mx, my = mymouse.position()
  buttons = mymouse.button_status()

  rot -= (mx - omx) * 0.1
  tilt += (my - omy) * 0.1
  omx=mx
  omy=my

  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # forward
      xm += CAMERA.mtrx[0, 3]
      ym += CAMERA.mtrx[1, 3]
      zm += CAMERA.mtrx[2, 3]
    elif k == ord('s'): # backwards
      xm -= CAMERA.mtrx[0, 3]
      ym -= CAMERA.mtrx[1, 3]
      zm -= CAMERA.mtrx[2, 3]

