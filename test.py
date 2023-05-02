import pyglet

window = pyglet.window.Window()
image = pyglet.resource.image('grl.png')

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()