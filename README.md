# ray-tracing

## abstract
the implementation is going to be completely vectorized through every step of the process, for loops will be avoided like the plague



local object cooordinates are transformed into world coordinates
when loaded into the scene. note: track where they are in the
world geometry array so they can be easily subbed out

## to do
geometry culling does not work for culling entire polygons, it needs to be able to receive structured lists to do that effectively
## learning materials
[playlist](https://www.youtube.com/playlist?list=PLW3Zl3wyJwWN6V7IEb2BojFYOlgpryp1-)
[ray plane intersection](https://www.youtube.com/watch?v=fIu_8b2n8ZM&list=PLW3Zl3wyJwWN6V7IEb2BojFYOlgpryp1-&index=3)
[ray triangle intersection](https://www.youtube.com/watch?v=EZXz-uPyCyA&list=PLW3Zl3wyJwWN6V7IEb2BojFYOlgpryp1-&index=8)
[projections](https://www.youtube.com/watch?v=VTV1GTrrtBQ&list=PLW3Zl3wyJwWN6V7IEb2BojFYOlgpryp1-&index=6)
[efficient triangle rasterization](https://www.youtube.com/watch?v=PahbNFypubE)

## steps in the rendering pipeline:
1. Application
    1. User Input
    2. Animation
2. Geometry
    1. model & camera transformation
    2. lighting
    3. projection
    4. clipping
    5. window->viewport transformation
3. Rasterization

transform world geometry into camera-relative geometry where the camera
faces into positive z for easy math


## features
textured materials
reflection and refraction
obj handling
radiance mapping
depth of field
shaders

## conventions

coordinate system: blender system,
right handed with z pointing upwards
rotation: positive is counter-clockwise

soh
cah
toa

sin of theta = opposite/hypotenuse
cos of theta = adjacent/hypotenuse
tan of theta = opposite/adjacent

## geometry  pipeline

1. object coordinates: vertexes are defined relative to their object origin
2. world coordinates: vertexes are defined relative to the world origin
3. camera space: vertexes are defined relative to the camera's perspective aka eye/view space
4. projection space: 2d points
4. clip space: 2d points where anything over |1| is out
5. screen space: coordinates that correspond to a position on the screen

