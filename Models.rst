.. highlight:: python
   :linenothreshold: 25

Models
======

3D models can be made and edited using a wide variety of software and
saved in nearly as large a variety of formats. In pi3d, at the moment,
there are just two file types that can be parsed: wavefront **obj** and
Panda3D **egg**. Of these two the obj is simpler and faster to load.

If you have **blender** [#]_ installed on your PC then you can open the
file **model01.blend** [#]_ or you can view it by running the pi3d demo
**model01.py** [#]_ It's basically a box with horns! In the diagram below
the left view is normal perspective (as with pi3d) and the right view is
the uv "unwrapping" for texture mapping to the vertices.

Blender screen

.. image:: blender01.jpg

Open the **blender01.obj** and **blender01.mtl** files and have a look at
the structure of the information, it should be reasonably familiar by now
with a little explanation.

Most of the obj file consists of four types of lines:

  **v vertex** lines with x, y, z coordinates.

  **vt vertex texture** lines with u, v coordinates.

  **vn vertex normal** lines with x, y, z components of normals.

  **f face** lines with a series of references to v/vt/vn lines for each
  corner of the face. When I made the model in blender I converted the
  faces to triangles but in general there could be more corners and the
  parser function has to convert it into triangles to work with OpenGL ES2.0

Additional occasional lines are **mtllib model01.mtl** which points to material file.
**o Cube** define different objects within this file. In pi3d these will
each be a different Buffer object within one Shape. **usemtl Material**
instructs the properties from mtllib under "Material" to be used for the
following faces. **s off** and **s 1** turn smoothing off and on. Pi3d
doesn't use these instruction but does use the normals. If you look at the
lines::

  s off
  f 4/1/1 11/2/1 3/3/1
  f 8/4/2 7/5/2 10/6/2
  f 9/7/3 14/8/3 22/9/3

You will see three faces using vertices (4,11,3) (8,7,10) (9,14,22) with
normals (1,1,1) (2,2,2) (3,3,3) i.e. all three corners are facing the same
direction. Later on::

  s 1
  f 22/9/15 30/62/16 23/63/17
  f 22/21/15 17/20/18 25/64/19
  f 30/62/16 38/65/20 31/66/21

faces (22,30,12) (22,17,25) (30,38,31) have normals (15,16,17) (15,18,19)
(16,20,21) i.e. not a flat face. And you will see that the same vertex
used in different faces (i.e. vertex #22 or #30 above) has the same normal vector
(#15 or #16)

In the mtl file you will see that there is a **newmtl Material** to match
the usemtl line in the obj file, followed by lines specifying material
properties (Ns specular exponent, Ka ambient, Kd diffuse, Ks specular (RGB
values), d alpha, illum illumination model, map_kd a file to use for diffuse
values) Pi3d only picks up the Kd and map_kd to use as material and Texture.

.. [#] http://www.blender.org/
.. [#] https://github.com/paddywwoof/pi3d_book/blob/master/model01.blend
.. [#] https://github.com/paddywwoof/pi3d_book/blob/master/model01.py
