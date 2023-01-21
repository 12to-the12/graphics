import pygame
import numpy as np
pygame.init()
display = pygame.display.set_mode((300, 300))
x = np.arange(0, 300)
y = np.arange(0, 300)
X, Y = np.meshgrid(x, y)
Z = X + Y
Z = 255*Z/Z.max()
print(Z.shape)
surf = pygame.surfarray.make_surface(Z)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display.blit(surf, (0, 0))
    pygame.display.update()
pygame.quit()