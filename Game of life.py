import pygame
import numpy as np
import time

pygame.init()

width, height = 700, 700

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Life Game")
pygame.display.set_icon(screen)
pygame.display.set_allow_screensaver(True)

negro = 25, 25, 25
gris = 128, 128, 128
blanco = 255, 255, 255

screen.fill(negro)


nxC, nyC = 60, 60

dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC))

clock = pygame.time.Clock()

name_font = pygame.font.SysFont('ubuntu', 25)
text1 = name_font.render("PAUSE", True, blanco)

pauseExect = True
game_over = True

while game_over:
    newGameState = np.copy(gameState)
    screen.fill(negro)
    time.sleep(0.05)

    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            game_over = False
            continue

        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

            if event.key == pygame.K_ESCAPE:
                game_over = False
                continue

            if event.key == pygame.K_z:
                gameState = np.zeros((nxC, nyC))
                newGameState = np.copy(gameState)
                pauseExect = not pauseExect
                continue

        mouseClick = pygame.mouse.get_pressed(3)

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

            pygame.draw.line(screen, blanco, [0, 0], [posX, posY], 2)

            if newGameState[celX, celY] == 1:
                newGameState[celX, celY] = 0
            else:
                newGameState[celX, celY] = 1

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[x % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, y % nyC] + \
                          gameState[(x + 1) % nxC, y % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[x % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Regla 1
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla 2
                if gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            if pauseExect:
                screen.blit(text1, [0, 0])

            poly = [(x * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (x * dimCW, (y + 1) * dimCH)]

            if newGameState[x, y] == 0:
                # pygame.draw.polygon(screen, gris, poly, 2)
                pass
            else:
                pygame.draw.polygon(screen, (60, 130, 200), poly, 3)
                pygame.draw.polygon(screen, blanco, poly, 0)

    gameState = np.copy(newGameState)
    # clock.tick(50)
    pygame.display.update()
