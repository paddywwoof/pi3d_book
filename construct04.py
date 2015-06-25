#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

from random import random

B_DIM = ((4.5, 3.5, 5.0), (3.0, 2.0, 3.0)) # width, depth, height
""" NB the notation here is x,y being dimensions of the block and locations
of corners etc. These really correspond to x,z in the 3D world

First are a couple of utility functions
"""
def interp(pt0, pt1, l):
  """ return a point distance l from pt0 (towards pt1)
  """
  dx, dy = pt1[0] - pt0[0], pt1[1] - pt0[1]
  L = (dx ** 2 + dy ** 2) ** 0.5
  return [pt0[0] + l / L * dx, pt0[1] + l / L * dy]

def shrink_block(block, f):
  """ produce a block scaled by f about average point
  """
  x_av, y_av = 0.0, 0.0
  for c in block:
    x_av += c[0]
    y_av += c[1]
  x_av /= len(block)
  y_av /= len(block)
  return [[f * c[0] + (1 - f) * x_av, f * c[1] + (1 - f) * y_av] for c in block]


def build_block_specs(block, o_prob=0.15):
  """ block is a list of corners (x,y)
  """
  ########## Corners ###################################################
  corners = [] # this will be a list of buildings each as c below
  n = len(block)
  for i in range(n):
    (x0,y0) = block[i] # corner point
    (x1,y1) = block[(i+1) % n] # next point clockwise
    (x2,y2) = block[i-1] # previous point (i.e. next anti-clockwise)
    # c will be a list of type followed by four corners of building
    c = [0 if random() < o_prob else 1] # choose between office or house
    var = (5.0 + random()) / 5.5 # variation
    # add three "outside" corners, clockwise order
    c.extend([interp((x0, y0), (x2, y2), B_DIM[c[0]][1] * var), [x0, y0],
              interp((x0, y0), (x1, y1), B_DIM[c[0]][0] * var)])
    m1 = float(x0 - x1) / (y1 - y0) # gradient right angle to street
    m2 = float(x0 - x2) / (y2 - y0) # gradient relative to other street
    # x3,y3 is intercept point
    x3 = float(c[1][1] - c[3][1] + m1 * c[3][0] - m2 * c[1][0]) / (m1 - m2)
    y3 = c[1][1] + m2 * (x3 - c[1][0])
    c.extend([[x3, y3]]) # add intercept as fourth corner
    corners.append(c)

  #################### now fill in the edges ###########################
  av_w = B_DIM[0][0] * o_prob + B_DIM[1][0] * (1.0 - o_prob) # average width
  edges = [] # will be filled with edges
  for i in range(n):
    (x0, y0) = corners[i-1][3] # ends of edge between corner buildings
    (x1, y1) = corners[i][1]
    slen = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 # length of edge
    nbuild = int(slen / av_w + 0.5) # number to fit in
    edge = [] # will be filled with buildings
    # first create a string of buildings at 45 degrees then work out scale
    # factors so they fit from x0y0 to x1y1
    x_last, y_last = 0.0, 0.0
    for j in range(nbuild):
      b = [0 if random() < o_prob else 1, [x_last, y_last]]
      width = B_DIM[b[0]][0] * (3.0 + random()) / 3.5
      x_last += width
      y_last += width
      b.append([x_last, y_last])
      edge.append(b)
    x_factor = (x1 - x0) / x_last if x_last != 0.0 else 0.0
    y_factor = (y1 - y0) / y_last if y_last != 0.0 else 0.0
    for b in edge:
      for j in b[1:3]:
        j[0] = x0 + j[0] * x_factor
        j[1] = y0 + j[1] * y_factor
      depth = B_DIM[b[0]][1] * (3.0 + random()) / 3.5
      dx = (y1 - y0) * depth / slen # line at right angle to edge
      dy = (x1 - x0) * depth / slen
      b.insert(1, [b[1][0] + dx, b[1][1] - dy]) # first point in spec at back
      b.append([b[3][0] + dx, b[3][1] - dy]) # last point in spec at at back
    edges.append(edge)

  #########  now make the lists to return ##############################
  office_specs = []
  house_specs = []
  for c in corners:
    if c[0] == 0: # it's an office
      office_specs.append(c[1:])
      ht = B_DIM[0][2] * (0.3 + random()) / 0.3
      office_specs[-1].extend([ht, ht / 20.0])
    else:
      house_specs.append(c[1:])
      ht = B_DIM[1][2] * (1.0 + random()) / 1.0
      house_specs[-1].extend([ht, 1.0])
  for edge in edges:
    for b in edge:
      if b[0] == 0: # it's an office
        office_specs.append(b[1:])
        ht = B_DIM[0][2] * (0.3 + random()) / 0.3
        office_specs[-1].extend([ht, ht / 20.0])
      else:
        house_specs.append(b[1:])
        ht = B_DIM[1][2] * (1.0 + random()) / 1.0
        house_specs[-1].extend([ht, 1.0])
  return (office_specs, house_specs)


""" Doing the conditional block below will allow this file to be imported
and the build_block_specs() function called but for development we can
run the file and this code will get executed.

To check it's doing what we want it gets drawn. At this scale for 3D objects
it would be very small so we overwrite the building dimesions "static
constant" variable B_DIM! making everything bigger.
"""
if __name__ == "__main__":
  from PIL import Image, ImageDraw
  B_DIM = ((55, 45, 50), (40, 25, 30)) # width, depth, height - for larger scale image
  off_specs, hou_specs = build_block_specs(((56,56),(36, 206),(206, 406),(356, 336),(296, 06))) # large scale image version
  im = Image.new("L", (512, 512), 255)
  draw = ImageDraw.Draw(im)
  for spec in off_specs:
    draw.line([i for j in spec[:4] for i in j] + spec[0], fill=0, width=2)
  for spec in hou_specs:
    draw.line([i for j in spec[:4] for i in j] + spec[0], fill=128, width=4)
  im.save("temp.png")

    

