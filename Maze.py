import pygame
from pygame.draw import line, rect
import numpy as np
import math

import random


class Maze:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale
        self.walls = None
        self.walls_color = (255, 255, 0)
        self.solutions = {}
        self.generate_maze()

    # Maze generation
    def generate_maze(self):
        self.walls = [
            np.ones((self.width, self.height + 1), dtype=bool),
            np.ones((self.width + 1, self.height), dtype=bool)
        ]

        current = (self.width // 2, self.height // 2)
        backtrack = [current]
        visited = [current]

        while len(backtrack) > 0:
            neighbours = self.get_neighbours(current)
            unvisited_neighbours = list(
                filter(lambda n: n not in visited, neighbours))
            if len(unvisited_neighbours) > 0:
                selected_neighbour = random.choice(unvisited_neighbours)
                self.remove_wall(current, selected_neighbour)
                backtrack.append(selected_neighbour)
                visited.append(selected_neighbour)
                current = selected_neighbour
            else:
                current = backtrack.pop()

    def remove_wall(self, f, t):
        dir_x = t[0] - f[0]
        dir_y = t[1] - f[1]

        if dir_x == 1:
            self.walls[1][t[0], t[1]] = False
        elif dir_x == -1:
            self.walls[1][f[0], f[1]] = False
        elif dir_y == 1:
            self.walls[0][t[0], t[1]] = False
        elif dir_y == -1:
            self.walls[0][f[0], f[1]] = False

    def get_neighbours(self, pos):
        neighbours = [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1)
        ]
        return list(filter(lambda n: self.contain(n), neighbours))

    def contain(self, pos):
        return pos[0] < self.width and pos[0] >= 0 and pos[1] < self.height and pos[1] >= 0

    # A star calculus
    def get_solution(self, start, goal):
        if (start, goal) in self.solutions:
            return self.solutions[(start, goal)]

        closed_set = set()
        open_set = {start}

        came_from = {}
        g_score = {}
        f_score = {}
        for x in range(self.width):
            for y in range(self.height):
                g_score[(x, y)] = math.inf
                f_score[(x, y)] = math.inf
        g_score[start] = 0
        f_score[start] = self.heuristic_cost_estimate(start, goal)

        while len(open_set) > 0:
            sorted_keys_f_score = sorted(open_set, key=lambda p: f_score[p])
            current = sorted_keys_f_score[0]

            if current == goal:
                self.solutions[(start, goal)] = self.reconstruct_path(came_from, current)
                return self.solutions[(start, goal)]

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in self.get_neighbours(current):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + self.dist_between(current, neighbor)

                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.heuristic_cost_estimate(neighbor, goal)

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return total_path

    def dist_between(self, f, t):
        dir_x = t[0] - f[0]
        dir_y = t[1] - f[1]

        if dir_x == 1:
            if self.walls[1][t[0], t[1]] == True:
                return math.inf
            else:
                return 1
        elif dir_x == -1:
            if self.walls[1][f[0], f[1]] == True:
                return math.inf
            else:
                return 1
        elif dir_y == 1:
            if self.walls[0][t[0], t[1]] == True:
                return math.inf
            else:
                return 1
        elif dir_y == -1:
            if self.walls[0][f[0], f[1]] == True:
                return math.inf
            else:
                return 1

    def heuristic_cost_estimate(self, f, t):
        return (f[0] - t[0]) ** 2 + (f[1] - t[1]) ** 2


    def mouse_pos(self):
        pos = pygame.mouse.get_pos()
        x = pos[0] // self.scale
        y = pos[1] // self.scale
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.width - 1:
            x = self.width - 1
        if y > self.height - 1:
            y = self.height - 1

        return (x, y)
    # Pygame draw function

    def draw(self, screen):
        for x in range(self.walls[0].shape[0]):
            for y in range(self.walls[0].shape[1]):
                if self.walls[0][x, y]:
                    start_pos = (x * self.scale, y * self.scale)
                    end_pos = ((x + 1) * self.scale, y * self.scale)
                    line(screen, self.walls_color, start_pos, end_pos)

        for x in range(self.walls[1].shape[0]):
            for y in range(self.walls[1].shape[1]):
                if self.walls[1][x, y]:
                    start_pos = (x * self.scale, y * self.scale)
                    end_pos = (x * self.scale, (y + 1) * self.scale)
                    line(screen, self.walls_color, start_pos, end_pos)

    def draw_path(self, screen, path):
        for a, b in zip(path, path[1:]):
            start_pos = (a[0] * self.scale + self.scale // 2, a[1] * self.scale + self.scale // 2)
            end_pos = (b[0] * self.scale + self.scale // 2, b[1] * self.scale + self.scale // 2)
            line(screen, (255, 0, 255), start_pos, end_pos)
