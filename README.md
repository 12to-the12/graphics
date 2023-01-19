# ray-tracing


the implementation is going to be completely vectorized through every step of the process, for loops will be avoided like the plague



local object cooordinates are transformed into world coordinates
when loaded into the scene. note: track where they are in the
world geometry array so they can be easily subbed out

## steps in the rendering pipeline:
transform world geometry into camera-relative geometry where the camera
faces into positive z for easy math


## features
textured materials
reflection and refraction
obj handling
radiance mapping

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

## coordinate space pipeline

1. object space: vertexes are defined relative to their object origin
2. world space:  vertexes are defined relative to the world origin
3. 