from src.scripts.camera import Camera


def test_camera():
    camera = Camera(
        aspect_ratio=1.0, focal_length=12, sensor_width=12, close_cull=0, far_cull=1
    )
    assert camera.focal_length == 12
