from src.scripts.camera import Camera
import math


def test_aspect_ratio():
    camera = Camera(
        sensor_height=12, focal_length=12, sensor_width=6, close_cull=0, far_cull=1
    )
    assert camera.aspect_ratio == 0.5


def test_fov():
    camera = Camera(
        sensor_height=10, focal_length=5, sensor_width=10, close_cull=0, far_cull=1
    )
    assert math.degrees(camera.fov) == 90


def test_focal_ratio():
    camera = Camera(
        sensor_height=12, focal_length=12, sensor_width=6, close_cull=0, far_cull=1
    )
    assert camera.aspect_ratio == 0.5


def test_fov():
    camera = Camera(
        sensor_height=24, focal_length=50, sensor_width=36, close_cull=0, far_cull=1
    )
    assert camera.aspect_ratio == 1.5
    assert round(math.degrees(camera.horizontal_field_of_view)) == 40
    assert round(math.degrees(camera.vertical_field_of_view)) == 27
    camera.focal_length = 30

    assert round(math.degrees(camera.horizontal_field_of_view)) == 62
    assert round(math.degrees(camera.vertical_field_of_view)) == 44
    camera.focal_length = 18
    assert round(math.degrees(camera.horizontal_field_of_view)) == 90
    assert round(math.degrees(camera.vertical_field_of_view)) == 67
