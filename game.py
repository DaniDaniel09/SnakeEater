"""
:author: Daniel Zanón Lopez/DaniDaniel09
"""

# These lines of code are importing necessary modules and classes for the game to run.
import time
from random import randint
import pygame
from pygame.locals import *
from player import Player
from render import Render


# TODO:  1) render to client
#        2) handle_event - handle msgs instead of pygame events

# This is a class for a game that involves players moving around a field, eating fruits, colliding
# with each other and the bounds, and keeping score.
class Game:
    update_time = 0.5
    frame_time = 0.1

    players = {}
    fruits = []
    leaderboard = {}

    def __init__(self):
        pygame.init()
        self.step_num = 0
        self.width = 0
        self.height = 0

    def set_field_size(self, w, h):
        self.width = w
        self.height = h

    def add_player(self, id):
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)
        self.players[id] = Player(id, x, y)

    def add_fruit(self):
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)
        self.fruits.append((x, y))

    def check_collisions(self):
        player_array = self.players.copy().items()

        for i, player in player_array:
            head = player.body[0]

            if head in player.body[1::]:
                self.leaderboard[self.players[i].id] = self.players[i].score
                del self.players[i]
                print("Collided with self")

            if (head[0] < 0 or head[0] >= self.width or
                    head[1] < 0 or head[1] >= self.height):
                self.leaderboard[self.players[i].id] = self.players[i].score
                del self.players[i]
                print("Collided with bounds:")

            if head in self.fruits:
                self.players[i].eat_fruit()
                self.players[i].grow_tail()  # this may put tail on top of the head
                self.fruits.remove(head)
                self.add_fruit()

            for j, other in player_array:
                if j == i:
                    continue
                
                if head in other.body:
                    index = other.body.index(head)
                    
                    if index == 0 and len(player.body)>=len(other.body):
                        del self.players[other.id]
                        for k in range(len(other.body)):
                            self.players[i].grow_tail()
                    
                    if index > 0:
                        self.players[other.id].cut_at(index)
                        self.players[i].grow_tail()

    def update(self):
        for i, player in self.players.items():
            self.players[i].move()

    def handle_events(self, id, key):
        left, right, up, down = 1, 2, 3, 4

        if key == left:
            self.players[id].set_velocity(1, 0)

        if key == right:
            self.players[id].set_velocity(-1, 0)

        if key == up:
            self.players[id].set_velocity(0, -1)

        if key == down:
            self.players[id].set_velocity(0, 1)

        print(key)

    def run_step(self):
        self.step_num += 1

        if self.step_num * self.frame_time == self.update_time:
            self.step_num = 0
            self.update()
            self.check_collisions()

            if len(self.players) == 0:  # game is over when there are no players left
                return False

        return True
