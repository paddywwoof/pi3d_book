#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d

display = pi3d.Display.create(w=800, h=600)

CAMERA = pi3d.Camera(is_3d=True)
shader = pi3d.Shader(vshader_source = """
precision mediump float;
attribute vec3 vertex;           // these are the array buffer objects defined in Buffer
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // [0] model movement in real coords, [1] in camera coords
uniform vec3 unib[4];
/* umult, vmult => unib[2][0:1] # these are defined in Buffer
   u_off, v_off => unib[3][0:1] */
uniform vec3 unif[20];
/* eye position => unif[6][0:3] # defined in Shape
 light position => unif[8][0:3] */

varying vec2 texcoordout; // these have values set in the vertex shader which
varying vec3 lightVector; // are picked up in the fragment shader. However    
varying float lightFactor;// their values "vary" by interpolating between vertices
varying vec3 normout;

void main(void) {
  if (unif[7][0] == 1.0) {                        // this is a point light and unif[8] is location
    vec4 vPosn = modelviewmatrix[0] * vec4(vertex, 1.0); // apply the model transformation matrix
    lightVector =  unif[8] - vec3(vPosn);  // to get vector from vertex to the light position
    lightFactor = pow(length(lightVector), -2.0); // inverse square law
    lightVector = normalize(lightVector);         // now convert to unit vector for direction
  } else {                                        // this is directional light
    lightVector = normalize(unif[8]) * -1.0;      // directional light
    lightFactor = 1.0;                            // constant brightness
  }
  lightVector.z *= -1.0;                          // fix r-hand axis
  normout = normalize(vec3(modelviewmatrix[0] * vec4(normal, 1.0))); // matrix multiplication   
  texcoordout = texcoord * unib[2].xy + unib[3].xy; // offset and mult for texture coords
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0); // matrix multiplication
  /* gl_Position is a pre-defined variable that has to be set in the vertex
  shader to define the vertex location in projection space. i.e. x and y
  are now screen coordinates and z is depth to determine which pixels are
  rendered in front or discarded. This matrix multiplication used the full
  projection matrix whereas normout used only the model transformation matrix*/
}
""",

fshader_source = """
precision mediump float;
uniform sampler2D tex0; // this is the texture object
uniform vec3 unib[4];
/*     blend cutoff => unib[0][2] # defined in Buffer */
uniform vec3 unif[20];
/*      shape alpha => unif[5][2] # defined in Shape
          light RGB => unif[9][0:3]
  light ambient RGB => unif[10][0:3] */


varying vec3 normout; // as sent from vertex shader
varying vec2 texcoordout;
varying vec3 lightVector;
varying float lightFactor;

void main(void) {
  gl_FragColor = texture2D(tex0, texcoordout); /* look up the basic RGBA value
  from the loaded Texture. This function also takes into account the distance
  of the pixel and will use lower resolution versions or mipmaps that were
  generated on creation (unless mipmaps=False was set)
  gl_FragColor is another of the pre-defined variables, representing the
  RGBA contribution to this pixel */
  //gl_FragColor = vec4(0.7, 0.1, 0.4, 0.9);   // try making it a "material" color by swapping with the line above
  if (gl_FragColor.a < unib[0][2]) discard;         // to allow rendering behind the transparent parts of this object
  float intensity = clamp(dot(lightVector, normout) * lightFactor, 0.0, 1.0); // adjustment of colour according to combined normal
  //float intensity = dot(lightVector, normout) * lightFactor; // try removing the 0 to 1 constraint (with point light)
  gl_FragColor.rgb *= (unif[9] * intensity + unif[10]); // directional lightcol * intensity + ambient lightcol
  gl_FragColor.a *= unif[5][2]; // finally modify the alpha with the Shape alpha
}
""")

l_vec = [0.7, -0.7, 2.5]
light = pi3d.Light(l_vec,
                   (0.8, 1.0, 0.9),
                   (0.1, 0.05, 0.05), is_point=False)
cube = pi3d.Cuboid(camera=CAMERA, w=1.5, h=1.5, d=1.5, z=4.0)
tex = pi3d.Texture("techy1.jpg")
#tex = pi3d.Texture("techy2.png", blend=True)
#pi3d.opengles.glDisable(pi3d.GL_CULL_FACE)
cube.set_draw_details(shader, [tex])
""" This takes essentially the same code as light01.py but brings the
Shader code inside to allow hacking. NB there is virtually no debugging
or feedback on errors when things go wrong inside the shader so proceed
with caution, making small changes that you can reverse easily!

You can try similar experiments to the previous illustration moving the
light vector and changing between point and directional light. With point
light notice that if you rotate the cube so the light is near to one corner
you occasionally get one triangle of a face being illuminated differently
from the other. This is a result of the way that interpolation is done and
most of the time it's not an issue, the alternative would be to do the
distance calculation for every pixel - this would be a lot more work for
the GPU.

Try swapping the ``vec4 texc = texture2D`` line from the fragment shader
for the following fixed material shade. Try altering RGBA values, including
values > 1.0 and < 0.0.

See what effect the ``clamp()`` function has on the intensity in the fragment
shader. It will only have any effect when using a point light near to a
vertex.

Also try swapping the texture from the jpg to the png file on the next line
with varying alpha. Change the blend argument between True and False. This
variable is picked up in Buffer.draw() (line 306) and used in the fragment
shader via unib[0][2] This allows pixels to be discarded with either a soft
edge (if blend=True) and values merged with anything already drawn at that
pixel, or with a hard edge (if False). Compare the sphere of clouds on the
Earth.py demo with the trees on ForestWalk.py

As a bonus experiment with the partially transparent png texture try enabling
the following line which disables `CULL_FACE`. This means you can see the
back of the walls of the box. However if you look carefully you will see
that the lighting is not calcualted correctly - we only have one set of
normals and they point outwards. To get the correct lighting effect you
would have to create a double walled cube.
"""
#####
light_obj = pi3d.Lines(vertices=((0.0,0.0,0.0), l_vec ,
                                [0.95 * l_vec[0], l_vec[1], l_vec[2]],
                                [l_vec[0], 0.95 * l_vec[1], l_vec[2]],
                                l_vec), line_width=4.0)
flatsh = pi3d.Shader("mat_flat")
light_obj.set_shader(flatsh)
#####
keys = pi3d.Keyboard()
while display.loop_running():
  cube.draw()
  light_obj.draw()

  k = keys.read()
  if k > -1:
    if k == 27:
      break
    elif k == ord('w'): # up
      l_vec[1] += 0.1
    elif k == ord('s'): # down
      l_vec[1] -= 0.1
    elif k == ord('a'): # left
      l_vec[0] -= 0.1
    elif k == ord('d'): # right
      l_vec[0] += 0.1
    elif k == ord('z'): # clockwise z
      cube.rotateIncZ(-2.5)
    elif k == ord('x'): # anti-clockwise z
      cube.rotateIncZ(2.5)
    elif k == ord('c'): # clockwise x
      cube.rotateIncX(-2.5)
    elif k == ord('v'): # anti-clockwise x
      cube.rotateIncX(2.5)
    elif k == ord('b'): # clockwise y
      cube.rotateIncY(-2.5)
    elif k == ord('n'): # anti-clockwise y
      cube.rotateIncY(2.5)
    light.position(l_vec)
    cube.set_light(light)
    light_obj = pi3d.Lines(vertices=((0.0,0.0,0.0), l_vec ,
                                  [0.95 * l_vec[0], l_vec[1], l_vec[2]],
                                  [l_vec[0], 0.95 * l_vec[1], l_vec[2]],
                                  l_vec), line_width=4.0)
    light_obj.set_shader(flatsh)

