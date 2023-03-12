from driver import set_xy, push, reset
from random import random
from time import sleep_ms
from webserver import get_pos
from math import sqrt

WIN = 7

class Game:
    def __init__(self):
        self.game_speed = 60
        self.x = 7.5
        self.y = 7.5

        self.vx = 0.2 * random()
        self.vy = 0.1 * random()

        self.p1 = 0
        self.p2 = 0

        self.p1_points = 0
        self.p2_points = 0


def show_score(game_state):
    pass


def tick(game_state):
    # get player positions
    p1, p2 = get_pos()
    game_state.p1 = p1
    game_state.p2 = p2

    # move ball
    game_state.x += game_state.vx
    game_state.y += game_state.vy

    # check collision
    if int(game_state.x) == 0:
        if game_state.p1 - int(game_state.y) < 3:
            game_state.vx = - game_state.vx
        else:
            game_state.x = 7.5
            game_state.y = 7.5
            game_state.vx = 0.2 * random()
            game_state.vy = 0.1 * random()
            game_state.p2_points += 1
            show_score(game_state)

            if game_state.p2_points == WIN:
                game_state = Game()


    elif int(game_state.x) == 15:
        if game_state.p2 - int(game_state.y) < 3:
            game_state.vx = -game_state.vx
        else:
            game_state.x = 7.5
            game_state.y = 7.5
            game_state.vx = 0.2 * random()
            game_state.vy = 0.1 * random()
            game_state.p1_points += 1
            show_score(game_state)

            if game_state.p1_points == WIN:
                game_state = Game()

    if int(game_state.y) == 0 or int(game_state.y) == 15:
        game_state.vy = - game_state.vy


    sleep_ms(int(1000 / game_state.game_speed))
    return game_state


def render(game_state):
    reset()

    #ball
    #todo interpolate ball
    set_xy(int(game_state.x), int(game_state.y), 0, 64, 0)
    set_xy(int(game_state.x - game_state.vx * 5), int(game_state.y - game_state.vy * 5), 0, 16, 0)
    set_xy(int(game_state.x - game_state.vx * 10), int(game_state.y - game_state.vy * 10), 0, 16, 0)


    # paddles
    set_xy(0, game_state.p1, 0, 0, 64)
    set_xy(0, game_state.p1 + 1, 0, 0, 64)
    set_xy(0, game_state.p1 + 2, 0, 0, 64)

    set_xy(15, game_state.p2, 64, 0, 0)
    set_xy(15, game_state.p2 + 1, 64, 0, 0)
    set_xy(15, game_state.p2 + 2, 64, 0, 0)
    push(wait=10)


def run_game():
    gs = Game()
    while True:
        gs = tick(gs)
        render(gs)
