import random
from collections import deque
import pyautogui

import pygame
import sys
from pygame.locals import *

#   pygame.display.Info().current_w
#   pygame.display.Info().current_h
GAME_CELL_SIZE_PX = 20
WIDTH, HEIGHT = pyautogui.size()
GAME_CELLS_X = WIDTH // GAME_CELL_SIZE_PX
GAME_CELLS_Y = (HEIGHT - 100) // GAME_CELL_SIZE_PX

FPS = 120
MPS = 10

FRAMES_PER_MOVE = FPS // MPS

random.seed(a=1)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)

background_color = BLACK


def draw_segment(surface, x, y, color):
    COLOR = color
    position = (
        x * GAME_CELL_SIZE_PX,
        y * GAME_CELL_SIZE_PX,
        GAME_CELL_SIZE_PX,
        GAME_CELL_SIZE_PX
    )
    pygame.draw.rect(surface, COLOR, position)


def draw_food(surface, x, y):
    RED = (255, 0, 0)
    position = (
        x * GAME_CELL_SIZE_PX + GAME_CELL_SIZE_PX // 2,
        y * GAME_CELL_SIZE_PX + GAME_CELL_SIZE_PX // 2
    )
    pygame.draw.circle(surface, RED, position, GAME_CELL_SIZE_PX // 2)


class Snake:
    vectors = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }

    def __init__(self, food):
        self.segments = deque([[GAME_CELLS_X - 0, GAME_CELLS_Y // 2], [GAME_CELLS_X - 1, GAME_CELLS_Y // 2],
                               [GAME_CELLS_X - 2, GAME_CELLS_Y // 2], [GAME_CELLS_X - 3, GAME_CELLS_Y // 2],
                               [GAME_CELLS_X - 4, GAME_CELLS_Y // 2], [GAME_CELLS_X - 5, GAME_CELLS_Y // 2]])
        self.direction = 'LEFT'
        self.last_direction = self.direction
        self.food = food

    def _normalize_segments(self):
        for segment in self.segments:

            if segment[0] >= GAME_CELLS_X:
                segment[0] -= GAME_CELLS_X
            if segment[0] < 0:
                segment[0] += GAME_CELLS_X
            if segment[1] >= GAME_CELLS_Y:
                segment[1] -= GAME_CELLS_Y
            if segment[1] < 0:
                segment[1] += GAME_CELLS_Y

    def move(self):
        vector = self.vectors.get(self.direction, (0, 0))
        self.last_direction = self.direction
        first_segment = self.segments[-1]
        self.segments.append(
            [first_segment[0] + vector[0], first_segment[1] + vector[1]]
        )
        self._normalize_segments()
        if not self.try_to_eat():
            self.segments.popleft()

    def draw(self, surface):
        for segment in self.segments:
            draw_segment(surface, *segment, (0, 0, 255))
        draw_segment(surface, *self.segments[-1], (255, 255, 255))

    def process_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if not self.last_direction == 'RIGHT':
                    self.direction = 'LEFT'
            elif event.key == K_RIGHT:
                if not self.last_direction == 'LEFT':
                    self.direction = 'RIGHT'
            elif event.key == K_UP:
                if not self.last_direction == 'DOWN':
                    self.direction = 'UP'
            elif event.key == K_DOWN:
                if not self.last_direction == 'UP':
                    self.direction = 'DOWN'

    def try_to_eat(self):
        if (
                self.segments[-1][0] == self.food.x
                and
                self.segments[-1][1] == self.food.y
        ):
            self.food.eaten()
            return True
        return False

    def check(self, snake):
        for segment in snake.segments:
            if self.segments[-1] == segment:
                return True
        for segment in self.segments:
            if self.segments[-1] == segment:
                if not self.segments[-1] is segment:
                    return True
        return False


class Snake2:
    vectors = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }

    def __init__(self, food):
        self.segments = deque(
            [[0, GAME_CELLS_Y // 2], [1, GAME_CELLS_Y // 2], [2, GAME_CELLS_Y // 2], [3, GAME_CELLS_Y // 2],
             [4, GAME_CELLS_Y // 2], [5, GAME_CELLS_Y // 2]])

        self.direction = 'RIGHT'
        self.last_direction = self.direction
        self.food = food
        self.color = (0, 255, 0)

    def _normalize_segments(self):
        for segment in self.segments:
            if segment[0] >= GAME_CELLS_X:
                segment[0] -= GAME_CELLS_X
            if segment[0] < 0:
                segment[0] += GAME_CELLS_X
            if segment[1] >= GAME_CELLS_Y:
                segment[1] -= GAME_CELLS_Y
            if segment[1] < 0:
                segment[1] += GAME_CELLS_Y

    def move(self):
        vector = self.vectors.get(self.direction, (0, 0))
        self.last_direction = self.direction
        first_segment = self.segments[-1]
        self.segments.append(
            [first_segment[0] + vector[0], first_segment[1] + vector[1]]
        )
        self._normalize_segments()
        if not self.try_to_eat():
            self.segments.popleft()

    def draw(self, surface):
        for segment in self.segments:
            draw_segment(surface, *segment, self.color)
        draw_segment(surface, *self.segments[-1], (255, 255, 255))

    def process_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                if not self.last_direction == 'RIGHT':
                    self.direction = 'LEFT'
            elif event.key == K_d:
                if not self.last_direction == 'LEFT':
                    self.direction = 'RIGHT'
            elif event.key == K_w:
                if not self.last_direction == 'DOWN':
                    self.direction = 'UP'
            elif event.key == K_s:
                if not self.last_direction == 'UP':
                    self.direction = 'DOWN'

    def try_to_eat(self):
        if (
                self.segments[-1][0] == self.food.x
                and
                self.segments[-1][1] == self.food.y
        ):
            self.food.eaten()
            return True
        return False

    def check(self, snake):
        for segment in snake.segments:
            if self.segments[-1] == segment:
                return True
        for segment in self.segments:
            if self.segments[-1] == segment:
                if not self.segments[-1] is segment:
                    return True
        return False


class FoodProvider:
    def __init__(self):
        self._get_new_cords()

    def _get_new_cords(self):
        self.x = random.randrange(GAME_CELLS_X)
        self.y = random.randrange(GAME_CELLS_Y)
        global MPS, FRAMES_PER_MOVE
        MPS = MPS + 1
        FRAMES_PER_MOVE = FPS // MPS

    def draw(self, surface):
        draw_food(surface, self.x, self.y)

    def eaten(self):
        global background_color
        background_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        self._get_new_cords()


def draw_background(surface):
    position = (
        0, 0,
        # GAME_CELLS_X * GAME_CELL_SIZE_PX,
        # GAME_CELLS_Y * GAME_CELL_SIZE_PX
        WIDTH,
        HEIGHT
    )
    position2 = (
        0, HEIGHT - 100,
        WIDTH,
        100
    )
    position3 = (
        0, HEIGHT - 100,
        WIDTH,
        10
    )
    pygame.draw.rect(surface, background_color, position)
    pygame.draw.rect(surface, GRAY, position2)
    pygame.draw.rect(surface, BLACK, position3)


def run_game():
    pygame.init()
    pygame.mixer.quit()

    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(
        (
            # GAME_CELLS_X * GAME_CELL_SIZE_PX,
            # GAME_CELLS_Y * GAME_CELL_SIZE_PX
            pygame.display.Info().current_w,
            pygame.display.Info().current_h
        )
    )
    pygame.display.set_caption('Moving segments with snake class')
    food = FoodProvider()
    snake = Snake(food=food)
    snake2 = Snake2(food=food)
    frames_elapsed_since_last_move = 0
    text = ''
    game_is_going = True
    font = pygame.font.SysFont(None, 100)
    while game_is_going:
        for event in pygame.event.get():
            # print('event: {}'.format(event))
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            snake.process_event(event)
            snake2.process_event(event)
        draw_background(DISPLAYSURF)
        snake.draw(DISPLAYSURF)
        snake2.draw(DISPLAYSURF)
        if snake2.check(snake):
            game_is_going = False
            text = 'arrows won'
        if snake.check(snake2):
            game_is_going = False
            text = 'wasd won'
        food.draw(DISPLAYSURF)
        frames_elapsed_since_last_move += 1
        if frames_elapsed_since_last_move >= FRAMES_PER_MOVE:
            frames_elapsed_since_last_move = 0
            snake.move()
            snake2.move()
        global MPS
        speed_text = 'speed: ' + str(MPS)
        wasd_text = 'wasd score: ' + str(len(snake2.segments) - 6)
        arrows_text = 'arrows score: ' + str(len(snake.segments) - 6)
        img = font.render(speed_text, True, (0, 0, 0))
        a = img.get_rect().width
        wasd_img = font.render(wasd_text, True, (0, 0, 0))
        arrows_img = font.render(arrows_text, True, (0, 0, 0))
        DISPLAYSURF.blit(img, (WIDTH // 2 - a // 2, HEIGHT - 80))
        DISPLAYSURF.blit(wasd_img, (WIDTH // 10, HEIGHT - 80))
        b = arrows_img.get_rect().width
        DISPLAYSURF.blit(arrows_img, (WIDTH - b - WIDTH // 10, HEIGHT - 80))
        pygame.display.update()
        fpsClock.tick(FPS)
    print(text)

    img = font.render(text, True, (0, 0, 0))

    while not game_is_going:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_is_going = True
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    global background_color
                    background_color = BLACK
                    MPS = 10
                    run_game()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        DISPLAYSURF.fill((255, 255, 255))
        DISPLAYSURF.blit(img, (20, 120))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    run_game()
