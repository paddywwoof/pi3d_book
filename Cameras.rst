.. highlight:: python
   :linenothreshold: 25

Cameras, 2D projection and Sprites
==================================

Although pi3d, and OpenGL generally, are aimed at making 3D rendering
efficient and fast they allow 2D rendering to be done equally well. In
fact we have already used 2D rendering in the first few examples in the
Vectors and Matrices chapter. In that chapter I mention in passing that 
for a 2D or ``orthographic`` projection the matrix multiplication simply
needs to preserve the x and y coordinates - no scaling with distance needs
to be done. I also mention that, in pi3d, this can be achieved by setting
the Camera argument is_3d=False.

So this is the general scheme for managing different types of rendering in
pi3d: Projection matrices are held in Camera objects. When a Shape is drawn
either an explicitly assigned Camera or a default one will be used and the
projection matrix passed to the shader as part of the ``uniform modelviewmatrix``
(as we saw at the end of the last chapter). Although it's possible to have
as many different Cameras as you want it's normally sufficient to have just
one 3D for rendering 3D objects that possibly moves around the virtual
environment under user control, and one 2D that remains fixed and allows
"dashboard" information to be displayed.

Have a look at the two demo programs Minimal.py and Minimal_2d.py from
https://github.com/pi3d/pi3d_demos There are a couple of noteworthy
differences between 3D and 2D projections:

  **Scale** In 3D projection (with the default lens settings) 1.0 unit of
  x or y at a z distance of 1.1 just about fills the screen (in the vertical
  direction; the ``field of view`` is defined vertically). Try adding variations
  of this line after the DISPLAY creation in Minimal.py::

    CAMERA = pi3d.Camera(lens=(1.0,    # near plane
                               1000.0, # far plane
                               25,     # field of view
                               DISPLAY.width / float(DISPLAY.height)))

  In 2D projections 1.0 unit of x or y equates to 1 pixel

  **z distance** In 2D projections the effective distance of objects (to
  determine what gets drawn in front of what) is::

    10000 / (10000 - z_2D)

  So if you set a 2D object at z=20.0 it will be drawn in front of a 3D
  object at z=1.002 (effectively in front of **all** 3D objects). To draw a
  2D object behind a 3D object at z=20.0 it must be moved to z=9500.0 However
  the relative positions of 2D objects with respect to each other work as
  you would expect so a 2D object drawn at z=20.0 is in front of a 2D object
  at z=21.0

In Minimal_2d.py try changing rotateIncZ to rotateIncX (or Y). Do you see
the effect of moving some of the object in front of the ``near plane``?
To keep it in view you need to move it further away. In the following line
``sprite.position()`` increase the z value from 5.0 to 50.0.

Open the demo file Blur.py. This has various features I haven't explained
yet: MergeShape, Defocus, Font and String. You can probably figure how they're
being used but don't worry about that at the moment. Just look at lines
78 and 79 where the String is defined. You will see that it uses a 2D
camera, try increasing the z value. The text will only coincide with the balls
when you increase z above 8000

The most common way to use the 2d Camera is with the Sprite class which maps
a rectangular Texture to a quad formed by two triangles. The Minimal_2d.py
demo above shows the basic use via the ImageSprite class which wraps up
the Texture loading and Shader allocation. Have a look at **sprites01.py** [#]_
which shows why the order of drawing objects matters for blending.

The Sprite class in pi3d is an easy way to do 2D rendering of images, however
it runs into processing limitations if it is used for sprites in the sense
of a 2D animation or game. Where there are hundreds or thousands of images
moving about (think "creeps + towers + missiles" in a tower defence game)
then it is more efficient to use the OpenGL point drawing functionality
which will be touched on in the chapter ``Lines and Points`` and demonstrated
in SpriteBalls.py and SpriteMulti.py

.. [#] https://github.com/paddywwoof/pi3d_book/blob/master/programs/sprites01.py
