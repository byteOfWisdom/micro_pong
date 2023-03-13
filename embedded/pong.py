from driver import set_xy, push, reset
from random import random
from time import sleep_ms
from receiver import get_pos, ready
from math import sqrt, sin, cos, pi

WIN = 7

class Game:
    def __init__(self):
        self.game_speed = 60
        self.x = 7.5
        self.y = 7.5

        self.vx = 0
        self.vy = 0
        self.randomize_velocity(0.15)

        self.p1 = 0
        self.p2 = 0

        self.p1_points = 0
        self.p2_points = 0


    def randomize_velocity(self, speed):
        self.vx = speed * sin(random() * 2 * pi)
        self.vy = speed * cos(random() * 2 * pi)


def show_score(game_state):
    reset()

    for s1 in range(game_state.p1_points):
        for y in range(15): set_xy(s1, y, 0, 0, 10)

    for s2 in range(game_state.p2_points):
        for y in range(15): set_xy(15 - s2, y, 10, 0, 0)

    push(2000)


def tick(game_state):
    # get player positions
    p1, p2 = get_pos()
    game_state.p1 = p1
    game_state.p2 = p2

    # move ball
    game_state.x += game_state.vx
    game_state.y += game_state.vy

    # check collision
    if round(game_state.x) == 0:
        if abs(game_state.p1 - round(game_state.y)) < 3:
            game_state.vx = - game_state.vx
        else:
            game_state.x = 7.5
            game_state.y = 7.5
            game_state.randomize_velocity(0.15)
            game_state.p2_points += 1
            show_score(game_state)

            if game_state.p2_points == WIN:
                game_state = Game()

    elif round(game_state.x) == 15:
        if abs(game_state.p2 - round(game_state.y)) < 3:
            game_state.vx = -game_state.vx
        else:
            game_state.x = 7.5
            game_state.y = 7.5
            game_state.randomize_velocity(0.15)
            game_state.p1_points += 1
            show_score(game_state)

            if game_state.p1_points == WIN:
                game_state = Game()

    if round(game_state.y) == 0 or round(game_state.y) == 15:
        game_state.vy = - game_state.vy

    sleep_ms(round(1000 / game_state.game_speed))
    return game_state


def render(game_state):
    reset()

    #ball
    #todo interpolate ball
    set_xy(round(game_state.x), round(game_state.y), 0, 64, 0)
    set_xy(round(game_state.x - game_state.vx * 5), round(game_state.y - game_state.vy * 5), 0, 16, 0)
    set_xy(round(game_state.x - game_state.vx * 10), round(game_state.y - game_state.vy * 10), 0, 1, 0)

    # paddles
    set_xy(0, game_state.p1, 0, 0, 64)
    set_xy(0, game_state.p1 + 1, 0, 0, 64)
    set_xy(0, game_state.p1 + 2, 0, 0, 64)

    set_xy(15, game_state.p2, 64, 0, 0)
    set_xy(15, game_state.p2 + 1, 64, 0, 0)
    set_xy(15, game_state.p2 + 2, 64, 0, 0)
    push(wait=10)


def run_game():
    reset()
    push()
    while not ready(): pass
    gs = Game()
    while True:
        gs = tick(gs)
        render(gs)
