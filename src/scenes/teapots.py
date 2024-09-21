print("<importing Scene>")
from scripts.scene import Scene
from utilities.alert import alert


def teapot_scene(config) -> Scene:
    from scripts.camera import Camera
    from scripts.object import Scene_Object, OBJ

    alert("<initializing camera>")
    camera = Camera(aspect_ratio=(config.window.h_res / config.window.v_res))
    camera.rotate(config.camera.pitch, axis="x")
    camera.translate(config.camera.location)

    triangle = OBJ("models/triangle")
    triangle.name = "triangle"

    cube = OBJ("models/cube")
    cube.name = "cube"

    # # cat = OBJ('models/cat')
    # # cat.name = 'cat'

    teapot = OBJ("models/teapot")
    teapot.name = "teapot"

    teapotb = OBJ("models/teapot")
    teapotb.name = "teapotb"

    teapotc = OBJ("models/teapot")
    teapotc.name = "teapotc"

    print("<importing Mesh>")
    from scripts.mesh import Mesh

    scene = Scene(camera=camera)
    scene.add_object(teapot)
    scene.add_object(teapotb)
    scene.add_object(teapotc)
    # scene.add_object( triangle )
    # scene.add_object( cube )

    teapot.rotate(90, axis="x", local=False)
    teapotb.rotate(90, axis="x", local=False)
    teapotc.rotate(90, axis="x", local=False)

    teapot.geometry_to_origin()
    teapotb.geometry_to_origin()
    teapotc.geometry_to_origin()
    # teapot.origin_to_geometry()

    teapotb.translate([-5, 0, 0])
    teapotc.translate([5, 0, 0])

    return scene
