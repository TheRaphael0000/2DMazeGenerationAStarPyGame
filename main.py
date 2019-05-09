import pygame
from pygame.draw import rect, circle
import numpy as np
from Maze import Maze

pygame.init()

W = 60
H = 40
SCALE = 20

start, goal = (0, 0), (W-1, H-1)

maze = Maze(W, H, SCALE)

WIDTH = SCALE * W
HEIGHT = SCALE * H
size = [WIDTH + 1, HEIGHT + 1]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Maze generation with A Star")

frame = 0
done = False
clock = pygame.time.Clock()
while not done:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if pygame.key.get_pressed()[pygame.K_q]:
        done = True
    if pygame.key.get_pressed()[pygame.K_r]:
        maze = Maze(W, H, SCALE)

    if pygame.mouse.get_pressed()[0]:
        start = maze.mouse_pos()
    if pygame.mouse.get_pressed()[2]:
        goal = maze.mouse_pos()

    screen.fill((14, 14, 14))
    maze.draw(screen)
    maze.draw_path(screen, maze.get_solution(start, goal))
    pygame.display.flip()
    frame += 1


pygame.quit()
